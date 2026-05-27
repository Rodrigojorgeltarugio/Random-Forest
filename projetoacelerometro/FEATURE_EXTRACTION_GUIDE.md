# Documentação: Função extract_accelerometer_features

## Descrição

A função `extract_accelerometer_features()` foi criada para extrair features otimizadas de dados de acelerômetro. Ela processa dados brutos (eixos x, y, z) e retorna **um DataFrame com uma única linha** contendo estatísticas calculadas.

---

## Assinatura

```python
def extract_accelerometer_features(df):
    """Extrai features otimizadas de dados de acelerômetro."""
    # df: pd.DataFrame ou np.ndarray com colunas x, y, z
    # Retorna: pd.DataFrame com 1 linha e 19 colunas
```

---

## Entrada

### Formato Aceito

#### 1. DataFrame com colunas x, y, z (com ou sem label)
```python
df = pd.DataFrame({
    'x': [0.05, -0.03, 0.01, ...],
    'y': [0.02, -0.04, 0.00, ...],
    'z': [9.79, 9.83, 9.78, ...],
    'label': ['parado', 'parado', ...]  # Opcional - será ignorada
})
```

#### 2. NumPy array com 3 colunas
```python
arr = np.array([
    [0.05, 0.02, 9.79],
    [-0.03, -0.04, 9.83],
    [0.01, 0.00, 9.78],
    ...
])
```

---

## Saída

### Estrutura do DataFrame

Um **DataFrame com exatamente 1 linha** contendo 19 colunas:

```python
Forma: (1, 19)
```

### Features Calculadas

#### Para cada eixo (x, y, z):

| Feature | Descrição | Fórmula |
|---------|-----------|---------|
| `{axis}_mean` | Média aritmética | Σx / n |
| `{axis}_std` | Desvio padrão | sqrt(Σ(x - mean)² / n) |
| `{axis}_var` | Variância | Σ(x - mean)² / n |
| `{axis}_min` | Valor mínimo | min(x) |
| `{axis}_max` | Valor máximo | max(x) |
| `{axis}_energy` | Energia (soma dos quadrados) | Σx² |

**Exemplo**: x_mean, x_std, x_var, x_min, x_max, x_energy, y_mean, y_std, ...

#### Features globais:

| Feature | Descrição | Fórmula |
|---------|-----------|---------|
| `magnitude_mean` | Média da magnitude | mean(sqrt(x² + y² + z²)) |

### Exemplo de Saída

```
   x_mean     x_std    x_var  x_min  x_max  x_energy  y_mean     y_std  ...  magnitude_mean
0   0.002  0.037014  0.00137  -0.04   0.05   0.0055       0  0.027386  ...        9.804087
```

---

## Características

✅ **Retorna DataFrame com UMA linha** (não múltiplas)  
✅ **Ignora coluna 'label' automaticamente**  
✅ **Suporta DataFrame e NumPy array**  
✅ **Nomes de colunas legíveis** (axis_feature)  
✅ **Cálculos de energia e magnitude**  
✅ **Sem valores NaN** (floats válidos)  

---

## Exemplos de Uso

### Exemplo 1: Arquivo CSV com label

```python
import pandas as pd
from utils import extract_accelerometer_features

# Carregar dados
df = pd.read_csv('dados.csv')  # com colunas x, y, z, label

# Extrair features
features = extract_accelerometer_features(df)

# Resultado
print(features.shape)  # (1, 19)
print(features['magnitude_mean'].values[0])  # 9.804087
```

### Exemplo 2: NumPy array

```python
import numpy as np
from utils import extract_accelerometer_features

# Criar array
arr = np.array([
    [0.05, 0.02, 9.79],
    [-0.03, -0.04, 9.83],
    [0.01, 0.00, 9.78],
])

# Extrair features
features = extract_accelerometer_features(arr)

# Resultado
print(features)  # DataFrame (1, 19)
```

### Exemplo 3: Processar múltiplos arquivos

```python
import pandas as pd
from utils import extract_accelerometer_features

arquivos = ['dados1.csv', 'dados2.csv', 'dados3.csv']
todos_features = []

for arquivo in arquivos:
    df = pd.read_csv(arquivo)
    features = extract_accelerometer_features(df)
    todos_features.append(features)

# Combinar todos
df_features = pd.concat(todos_features, ignore_index=True)
print(df_features.shape)  # (3, 19) - 3 arquivos, 19 features cada
```

---

## Compatibilidade

### Função Antiga Mantida

A função original `extract_features_from_array()` continua disponível para compatibilidade com código legado:

```python
from utils import extract_features_from_array

# Retorna dicionário (não DataFrame)
features_dict = extract_features_from_array(arr)
```

**Diferenças:**
- `extract_features_from_array()` → retorna dicionário
- `extract_accelerometer_features()` → retorna DataFrame (NOVA ✨)

---

## Tratamento de Erros

### Erro: Colunas faltando

```python
# ❌ Erro se faltar coluna
df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})  # Falta 'z'
extract_accelerometer_features(df)
# ValueError: Faltam colunas: ['z']
```

### Solução: Garantir que as 3 colunas existem

```python
# ✅ Correto
df = pd.DataFrame({
    'x': [0.05, -0.03],
    'y': [0.02, -0.04],
    'z': [9.79, 9.83]
})
features = extract_accelerometer_features(df)
```

---

## Desempenho

- ⚡ Otimizado com NumPy e Pandas
- 📊 Rápido mesmo com grandes datasets
- 💾 Retorna sempre 1 linha (formato compacto)

---

## Use Cases

✅ Preparar dados para **Machine Learning**  
✅ Extrair features de **sensores de acelerômetro**  
✅ Análise de **movimento e atividades**  
✅ Classificação de **tipos de movimento**  
✅ Feature engineering em **time-series**  

---

## Integração com app.py

A função pode ser usada no endpoint `/process` com tarefa `extract`:

```python
# Em app.py
from utils import extract_accelerometer_features

features_df = extract_accelerometer_features(df)
# Salvar em CSV
features_df.to_csv(f'{job_id}_features.csv', index=False)
```

---

## Comparação: Antes vs Depois

### Antes (extract_features_from_array)
```python
# Retorna dicionário com muitas features
{
    'a0_mean': 0.002,
    'a0_std': 0.037,
    'a0_median': 0.01,
    'a0_iqr': 0.05,
    ...  # 30+ features
}
```

### Depois (extract_accelerometer_features)
```python
# Retorna DataFrame com 1 linha
   x_mean  x_std  x_var  x_min  x_max  x_energy  y_mean  ...  magnitude_mean
0   0.002  0.037  0.001  -0.04  0.05    0.0055       0  ...        9.804087
```

**Benefícios:**
- ✅ Mais claro e direto
- ✅ Nomes de colunas significativos
- ✅ Sem coluna 'label'
- ✅ Inclui magnitude
- ✅ Fácil de usar com DataFrame

---

## Veja Também

- [test_new_features.py](test_new_features.py) - Exemplos de teste
- [app.py](app.py) - Integração com o sistema
- [EXEMPLO_PRATICO.md](EXEMPLO_PRATICO.md) - Exemplos práticos

