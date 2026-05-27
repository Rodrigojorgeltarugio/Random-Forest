import pandas as pd
import numpy as np

def extract_accelerometer_features(df):
    """
    Extrai features de dados de acelerômetro.
    
    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame com colunas 'x', 'y', 'z' (e opcionalmente 'label')
    
    Retorno:
    --------
    pd.DataFrame
        Um DataFrame com UMA linha contendo todas as features calculadas
        
    Features calculadas para cada eixo (x, y, z):
    - mean: média aritmética
    - std: desvio padrão
    - var: variância
    - min: valor mínimo
    - max: valor máximo
    - energy: soma dos quadrados (energia)
    
    Features globais:
    - magnitude_mean: média da magnitude do vetor (x, y, z)
    """
    
    # Converter para DataFrame se necessário
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df, columns=['x', 'y', 'z'])
    
    # Selecionar apenas as colunas numéricas relevantes (x, y, z)
    # Ignorar 'label' se existir
    numeric_cols = [col for col in df.columns if col in ['x', 'y', 'z']]
    
    if len(numeric_cols) < 3:
        raise ValueError("DataFrame deve ter colunas 'x', 'y' e 'z'")
    
    # Manter ordem: x, y, z
    numeric_cols = ['x', 'y', 'z']
    df_data = df[numeric_cols].astype(float)
    
    # Dicionário para armazenar features
    features = {}
    
    # Calcular features para cada eixo
    for axis in numeric_cols:
        col = df_data[axis]
        
        features[f'{axis}_mean'] = col.mean()
        features[f'{axis}_std'] = col.std()
        features[f'{axis}_var'] = col.var()
        features[f'{axis}_min'] = col.min()
        features[f'{axis}_max'] = col.max()
        features[f'{axis}_energy'] = (col ** 2).sum()
    
    # Calcular magnitude média: sqrt(x² + y² + z²)
    magnitude = np.sqrt(df_data['x']**2 + df_data['y']**2 + df_data['z']**2)
    features['magnitude_mean'] = magnitude.mean()
    
    # Retornar como DataFrame com UMA linha
    return pd.DataFrame([features])


if __name__ == '__main__':
    # Exemplo de uso
    print("=== TESTE DA FUNÇÃO extract_accelerometer_features ===\n")
    
    # Criar DataFrame de exemplo
    data = {
        'x': [0.05, -0.03, 0.01, 0.02, -0.04],
        'y': [0.02, -0.04, 0.00, -0.01, 0.03],
        'z': [9.79, 9.83, 9.78, 9.82, 9.80],
        'label': ['parado', 'parado', 'parado', 'parado', 'parado']
    }
    
    df = pd.DataFrame(data)
    
    print("Entrada (DataFrame):")
    print(df)
    print(f"\nForma: {df.shape}")
    
    # Extrair features
    features_df = extract_accelerometer_features(df)
    
    print("\n" + "="*70)
    print("Saída (Features):")
    print(features_df)
    print(f"\nForma: {features_df.shape}")
    
    print("\n" + "="*70)
    print("Features calculadas:")
    for col in features_df.columns:
        print(f"  {col}: {features_df[col].values[0]:.6f}")
