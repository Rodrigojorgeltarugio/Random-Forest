from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from utils import load_file_as_array, extract_features_from_array, expand_archive, list_supported_files
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


def normalize_movement_label(value):
    raw = str(value).strip().lower()
    mapping = {
        '0': 'parado',
        '1': 'andando',
        '2': 'correndo',
        'stopped': 'parado',
        'stop': 'parado',
        'standing': 'parado',
        'parado': 'parado',
        'walk': 'andando',
        'walking': 'andando',
        'andando': 'andando',
        'run': 'correndo',
        'running': 'correndo',
        'correndo': 'correndo',
    }
    return mapping.get(raw, str(value))


def save_uploaded_files(files, job_id):
    saved = []
    job_folder = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_folder, exist_ok=True)
    for f in files:
        filename = secure_filename(f.filename)
        path = os.path.join(job_folder, filename)
        f.save(path)
        saved.append(path)
    return saved, job_folder


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    task = request.form.get('task')
    files = request.files.getlist('files')
    model_file = request.files.get('model')

    job_id = str(uuid.uuid4())
    saved_files, job_folder = save_uploaded_files(files, job_id)

    # Expand archives and build a flat list of files to process.
    all_files = []
    labels_map = {}
    for path in saved_files:
        lower = path.lower()
        if lower.endswith('.zip'):
            extracted = expand_archive(path, dest_dir=os.path.join(job_folder, os.path.splitext(os.path.basename(path))[0] + '_extracted'))
            # detect labels files first
            for f in extracted:
                bn = os.path.basename(f).lower()
                if bn in ('labels.csv', 'labels.json'):
                    try:
                        if bn.endswith('.csv'):
                            import pandas as _pd
                            df_labels = _pd.read_csv(f)
                            if 'filename' in df_labels.columns and 'label' in df_labels.columns:
                                for _, r in df_labels.iterrows():
                                    labels_map[str(r['filename'])] = r['label']
                        else:
                            import json as _json
                            with open(f, 'r', encoding='utf-8') as _fj:
                                data = _json.load(_fj)
                                # expect mapping {filename: label}
                                if isinstance(data, dict):
                                    for k, v in data.items():
                                        labels_map[k] = v
                    except Exception:
                        pass
            # append supported files
            supported = list_supported_files(extracted)
            all_files.extend(supported)
        else:
            all_files.append(path)

    # fallback: if no files after expansion, use saved_files
    if not all_files:
        all_files = saved_files

    if task == 'extract':
        rows = []
        for path in all_files:
            arrays = load_file_as_array(path)
            if arrays is None:
                continue
            # arrays could be multi-sensor or multi-samples; normalize to 2D
            feats = extract_features_from_array(arrays)
            feats['filename'] = os.path.basename(path)
            rows.append(feats)
        if not rows:
            return 'No valid files uploaded.', 400
        df = pd.DataFrame(rows)
        out_path = os.path.join(OUTPUT_DIR, f'{job_id}_features.csv')
        df.to_csv(out_path, index=False)
        return render_template('result.html', links=[url_for('download', filename=os.path.basename(out_path))])

    if task == 'train':
        X = []
        y = []
        sample_files = []
        feature_names = None
        for path in all_files:
            arrays = load_file_as_array(path)
            if arrays is None:
                continue
            feats = extract_features_from_array(arrays)
            if feature_names is None:
                feature_names = list(feats.keys())
            # Attempt to infer label: if file is CSV and contains 'label' column, load
            label = None
            bn = os.path.basename(path)
            # 1) check extracted labels_map (from labels.csv/json inside archive)
            if bn in labels_map:
                label = labels_map[bn]
            # 2) if csv file has a label column
            if label is None and path.lower().endswith('.csv'):
                try:
                    df_in = pd.read_csv(path)
                    if 'label' in df_in.columns:
                        label = df_in['label'].iloc[0]
                except Exception:
                    label = None
            # 3) infer from filename prefix before first underscore
            if label is None:
                if '_' in bn:
                    label = bn.split('_')[0]
            if label is None:
                # skip files without labels
                continue
            X.append(list(feats.values()))
            y.append(label)
            sample_files.append(bn)

        if len(X) < 2:
            # build diagnostics to help user
            diag = []
            for path in all_files:
                bn = os.path.basename(path)
                detected = None
                if bn in labels_map:
                    detected = labels_map[bn]
                elif path.lower().endswith('.csv'):
                    try:
                        df_in = pd.read_csv(path)
                        if 'label' in df_in.columns:
                            detected = df_in['label'].iloc[0]
                    except Exception:
                        detected = None
                elif '_' in bn:
                    detected = bn.split('_')[0]
                diag.append({'filename': bn, 'detected_label': detected})
            ddf = pd.DataFrame(diag)
            out_path = os.path.join(OUTPUT_DIR, f'{job_id}_train_diagnostic.csv')
            ddf.to_csv(out_path, index=False)
            return render_template('result.html', links=[url_for('download', filename=os.path.basename(out_path))], msg='Not enough labeled samples. Diagnostic CSV generated.')

        X = np.array(X)
        y = np.array(y)
        clf = RandomForestClassifier(n_estimators=100)

        # attempt a simple train/test split to report metrics
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        except Exception:
            # fallback if stratify impossible (small samples)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf.fit(X_train, y_train)

        # save model
        model_path = os.path.join(OUTPUT_DIR, f'{job_id}_rf_model.joblib')
        joblib.dump({'model': clf, 'feature_names': feature_names}, model_path)

        # compute metrics
        y_pred = clf.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred)) if len(y_test) > 0 else None
        cls_report = classification_report(y_test, y_pred, output_dict=True) if len(y_test) > 0 else {}
        cm = confusion_matrix(y_test, y_pred) if len(y_test) > 0 else None

        # prepare Excel report
        try:
            report_path = os.path.join(OUTPUT_DIR, f'{job_id}_training_report.xlsx')
            with pd.ExcelWriter(report_path) as writer:
                # metadata
                meta = pd.DataFrame([{
                    'job_id': job_id,
                    'model_type': 'RandomForestClassifier',
                    'n_estimators': 100,
                    'n_samples': len(X),
                    'n_features': X.shape[1]
                }])
                meta.to_excel(writer, sheet_name='metadata', index=False)

                # feature importances
                fi = pd.DataFrame({
                    'feature': feature_names,
                    'importance': clf.feature_importances_
                })
                fi.sort_values('importance', ascending=False).to_excel(writer, sheet_name='feature_importances', index=False)

                # training samples
                samples_df = pd.DataFrame({'filename': sample_files, 'label': list(y)})
                samples_df.to_excel(writer, sheet_name='training_samples', index=False)

                # metrics
                if cls_report:
                    metrics_df = pd.DataFrame(cls_report).transpose()
                    metrics_df.to_excel(writer, sheet_name='classification_report')
                if cm is not None:
                    cm_df = pd.DataFrame(cm)
                    cm_df.to_excel(writer, sheet_name='confusion_matrix', index=False)

            links = [url_for('download', filename=os.path.basename(report_path)), url_for('download', filename=os.path.basename(model_path))]
            return render_template('result.html', links=links)
        except Exception:
            # fallback: return model only
            return render_template('result.html', links=[url_for('download', filename=os.path.basename(model_path))])

    if task == 'predict':
        # model can be uploaded or we can use latest model in outputs
        model_obj = None
        if model_file and model_file.filename:
            tmp_model_path = os.path.join(job_folder, secure_filename(model_file.filename))
            model_file.save(tmp_model_path)
            model_obj = joblib.load(tmp_model_path)
        else:
            # pick latest model in OUTPUT_DIR
            mods = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.joblib')]
            if not mods:
                return 'No model available for prediction. Upload a model or train one first.', 400
            latest = max(mods, key=lambda n: os.path.getmtime(os.path.join(OUTPUT_DIR, n)))
            model_obj = joblib.load(os.path.join(OUTPUT_DIR, latest))

        clf = model_obj['model']
        feature_names = model_obj.get('feature_names')

        rows = []
        for path in all_files:
            arrays = load_file_as_array(path)
            if arrays is None:
                continue
            feats = extract_features_from_array(arrays)
            X = np.array([list(feats.values())])
            pred = clf.predict(X)
            probs = clf.predict_proba(X) if hasattr(clf, 'predict_proba') else None
            movement = normalize_movement_label(pred[0])
            row = {
                'filename': os.path.basename(path),
                'prediction': pred[0],
                'movement': movement,
            }
            if probs is not None:
                # include probability for predicted class
                try:
                    class_index = list(clf.classes_).index(pred[0])
                    row['probability'] = float(probs[0][class_index])
                except Exception:
                    row['probability'] = ''
            rows.append(row)

        if not rows:
            return 'No valid files for prediction.', 400
        df = pd.DataFrame(rows)
        out_path = os.path.join(OUTPUT_DIR, f'{job_id}_predictions.csv')
        df.to_csv(out_path, index=False)
        return render_template(
            'result.html',
            links=[url_for('download', filename=os.path.basename(out_path))],
            msg='Predição concluída. O status do movimento aparece na coluna movement.',
            rows=rows,
        )

    return 'Unknown task', 400


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
