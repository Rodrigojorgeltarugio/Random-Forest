import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def extract_features(df):
    """Extrai features de um DataFrame com colunas x, y, z.

    Se a coluna label existir, ela é ignorada.
    Retorna um DataFrame com uma única linha.
    """
    if isinstance(df, str):
        df = pd.read_csv(df)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    required = ['x', 'y', 'z']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Coluna(s) ausente(s): {missing}. O arquivo precisa ter x, y e z.")

    try:
        data = df[required].apply(pd.to_numeric, errors='raise')
    except Exception as exc:
        invalid = []
        for col in required:
            try:
                pd.to_numeric(df[col], errors='raise')
            except Exception:
                invalid.append(col)
        if invalid:
            raise ValueError(f"Coluna(s) inválida(s) ou não numérica(s): {invalid}") from exc
        raise

    features = {}
    for axis in required:
        series = data[axis]
        features[f'{axis}_mean'] = float(series.mean())
        features[f'{axis}_std'] = float(series.std())
        features[f'{axis}_min'] = float(series.min())
        features[f'{axis}_max'] = float(series.max())
        features[f'{axis}_energy'] = float((series ** 2).sum())

    return pd.DataFrame([features])


def train_model(df, model_path):
    """Treina um RandomForestClassifier com colunas x, y, z e label."""
    if isinstance(df, str):
        df = pd.read_csv(df)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    required = ['x', 'y', 'z', 'label']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Coluna(s) ausente(s): {missing}. Para treinar, o arquivo precisa ter x, y, z e label.")

    data = df[['x', 'y', 'z']].apply(pd.to_numeric, errors='raise')
    y = df['label']

    if len(df) < 2:
        raise ValueError('É necessário ter pelo menos duas linhas para treinar o modelo.')

    class_counts = y.value_counts()
    use_stratify = y.nunique() > 1 and class_counts.min() >= 2 and len(df) > y.nunique()
    if use_stratify:
        test_size = max(0.2, y.nunique() / len(df))
        test_size = min(test_size, 0.5)
    else:
        test_size = 0.5

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            data,
            y,
            test_size=test_size,
            random_state=42,
            stratify=y if use_stratify else None,
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            data,
            y,
            test_size=0.5,
            random_state=42,
            stratify=None,
        )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    if len(X_test) > 0:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
    else:
        accuracy = 1.0

    joblib.dump(model, model_path)
    return model, accuracy


def load_model(model_path):
    """Carrega um modelo salvo com joblib."""
    model = joblib.load(model_path)
    if isinstance(model, dict) and 'model' in model:
        return model['model']
    return model


def predict_model(model, df):
    """Executa predição para dados de acelerômetro."""
    if isinstance(df, str):
        df = pd.read_csv(df)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    required = ['x', 'y', 'z']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Coluna(s) ausente(s): {missing}. Para prever, o arquivo precisa ter x, y e z.")

    data = df[required].apply(pd.to_numeric, errors='raise')
    predictions = model.predict(data)

    return pd.DataFrame({
        'Amostra': list(range(1, len(predictions) + 1)),
        'Resultado': predictions,
    })
