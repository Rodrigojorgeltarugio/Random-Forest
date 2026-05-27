from flask import Flask, render_template, request, send_from_directory, url_for
import os
import uuid

import pandas as pd

from ml_models import extract_features, load_model, predict_model, train_model


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


def read_uploaded_dataframe(uploaded_file):
    """Lê um CSV enviado tentando encodings comuns."""
    read_errors = []
    for encoding in (None, 'utf-8', 'latin1'):
        try:
            uploaded_file.seek(0)
            if encoding is None:
                return pd.read_csv(uploaded_file)
            return pd.read_csv(uploaded_file, encoding=encoding)
        except Exception as exc:
            read_errors.append(f"{encoding or 'default'}: {exc}")

    raise ValueError(
        'Não foi possível ler o arquivo enviado como CSV. Verifique se o arquivo é válido. '
        + ' | '.join(read_errors)
    )


def render_error(message):
    return render_template(
        'results.html',
        result=f'<div class="alert alert-danger">{message}</div>',
        links=[],
        msg='',
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    task = request.form.get('task')
    uploaded = request.files.get('file')
    model_file = request.files.get('model')
    job_id = str(uuid.uuid4())

    if not uploaded or not uploaded.filename:
        return render_error('Nenhum arquivo enviado. Selecione um CSV com as colunas esperadas.')

    try:
        df = read_uploaded_dataframe(uploaded)
    except ValueError as exc:
        return render_error(str(exc))

    if task == 'extract':
        try:
            features_df = extract_features(df)
            result_html = features_df.to_html(classes='table table-striped table-bordered', index=False)
            return render_template('results.html', result=result_html, links=[], msg='')
        except ValueError as exc:
            return render_error(str(exc))
        except Exception as exc:
            return render_error(f'Ocorreu um erro ao extrair features: {exc}')

    if task == 'train':
        try:
            model_path = os.path.join(OUTPUT_DIR, 'latest_rf_model.joblib')
            _, accuracy = train_model(df, model_path)
            result_html = (
                '<div class="alert alert-success">Modelo treinado com sucesso</div>'
                f'<div class="alert alert-info">Acurácia: {accuracy * 100:.2f}%</div>'
            )
            links = [url_for('download', filename=os.path.basename(model_path))]
            return render_template('results.html', result=result_html, links=links, msg='')
        except ValueError as exc:
            return render_error(str(exc))
        except Exception as exc:
            return render_error(f'Ocorreu um erro ao treinar o modelo: {exc}')

    if task == 'predict':
        try:
            if model_file and model_file.filename:
                model_path = os.path.join(UPLOAD_DIR, job_id, model_file.filename)
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                model_file.seek(0)
                model_file.save(model_path)
            else:
                models = [name for name in os.listdir(OUTPUT_DIR) if name.endswith('.joblib')]
                if not models:
                    return render_error('Nenhum modelo disponível. Treine um modelo antes de prever.')
                model_path = os.path.join(
                    OUTPUT_DIR,
                    max(models, key=lambda name: os.path.getmtime(os.path.join(OUTPUT_DIR, name))),
                )

            model = load_model(model_path)
            predictions_df = predict_model(model, df)
            result_html = predictions_df.to_html(classes='table table-striped', index=False)
            return render_template('results.html', result=result_html, links=[], msg='')
        except ValueError as exc:
            return render_error(str(exc))
        except Exception as exc:
            return render_error(f'Ocorreu um erro ao prever: {exc}')

    return render_error('Tarefa desconhecida.')


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
