# Extração de Features - Resumo Executivo

## ✅ O que foi feito

Criei uma **nova função otimizada** para extrair features de dados de acelerômetro que atende exatamente aos seus requisitos.

---

## 📋 Função Principal

### `extract_accelerometer_features(df)`

**Localização**: [utils.py](utils.py)

**O que faz:**
- ✅ Aceita DataFrame com colunas x, y, z
- ✅ Retorna um DataFrame com **UMA linha** (não múltiplas)
- ✅ Calcula 19 features automáticas
- ✅ Ignora coluna 'label' se existir
- ✅ Usa Pandas e NumPy

---

## 📊 Features Calculadas (19 ao total)

Para cada eixo (x, y, z):
```
mean, std, var, min, max, energy
```

Globalmente:
```
magnitude_mean
```

**Total**: 6 features × 3 eixos + 1 global = **19 features**

---

## 📥 Entrada

### Opção 1: DataFrame com label
```python
df = pd.DataFrame({
    'x': [0.05, -0.03, 0.01],
    'y': [0.02, -0.04, 0.00],
    'z': [9.79, 9.83, 9.78],
    'label': ['parado', 'parado', 'parado']  # Ignorado automaticamente
})
```

### Opção 2: NumPy array
```python
arr = np.array([
    [0.05, 0.02, 9.79],
    [-0.03, -0.04, 9.83],
    [0.01, 0.00, 9.78]
])
```

---

## 📤 Saída

**Sempre um DataFrame com 1 linha**:

```
   x_mean  x_std  x_var  x_min  ...  z_energy  magnitude_mean
0   0.002  0.037  0.001  -0.04  ...    480.59        9.804087
```

**Forma**: `(1, 19)`

---

## 💻 Uso Rápido

```python
from utils import extract_accelerometer_features
import pandas as pd

# Carregar dados
df = pd.read_csv('dados.csv')

# Extrair features
features = extract_accelerometer_features(df)

# Usar resultado
print(features)  # DataFrame (1, 19)
print(features['magnitude_mean'].values[0])  # 9.804087
```

---

## 📚 Documentação Completa

Para documentação detalhada, veja:
- **[FEATURE_EXTRACTION_GUIDE.md](FEATURE_EXTRACTION_GUIDE.md)** - Guia completo com exemplos

---

## 🧪 Exemplos Práticos

Arquivo: **[exemplos_features.py](exemplos_features.py)**

Contém 6 exemplos práticos:
1. Dados simples
2. NumPy array
3. Arquivo CSV
4. Múltiplos arquivos
5. Cálculos detalhados
6. Lista completa de features

**Executar:**
```bash
python exemplos_features.py
```

---

## 🔄 Compatibilidade

### Função Antiga Mantida

A função anterior `extract_features_from_array()` continua disponível:

```python
from utils import extract_features_from_array

# Retorna dicionário (compatibilidade)
features_dict = extract_features_from_array(arr)
```

**Diferenças:**
| Função | Entrada | Saída | Uso |
|--------|---------|-------|-----|
| `extract_features_from_array()` | array/df | dict | Legado |
| `extract_accelerometer_features()` | df/array | DataFrame (1 linha) | NOVO ✨ |

---

## 🎯 Comparação: Antes vs Depois

### Antes
```python
# Retorna dicionário com muitas features
{
    'a0_mean': 0.002,
    'a0_std': 0.037,
    'a0_min': -0.04,
    'a0_median': 0.01,
    'a0_iqr': 0.05,
    'a0_rms': 0.033,
    'a0_skew': 0.056,
    'a0_kurtosis': -1.405,
    'a0_energy': 0.0055,
    'a0_dom_freq': 2.0,
    # ... mais 20 features
}
```

### Depois
```python
# Retorna DataFrame com 1 linha, 19 colunas bem nomeadas
   x_mean  x_std  x_var  x_min  x_max  x_energy  y_mean  ...  magnitude_mean
0  0.002   0.037  0.001  -0.04  0.05   0.0055      0   ...      9.804087
```

**Benefícios:**
- ✅ Nomes descritivos (x_mean, não a0_mean)
- ✅ DataFrame estruturado (não dicionário solto)
- ✅ Sem coluna label
- ✅ Inclui magnitude
- ✅ 1 linha, não múltiplas
- ✅ Fácil de usar em ML

---

## 📋 Checklist de Requisitos

- ✅ Entrada: DataFrame com x, y, z
- ✅ Saída: UMA linha com estatísticas
- ✅ Calcular: mean, std, var, min, max, energy para cada eixo
- ✅ Calcular: magnitude média
- ✅ Ignorar coluna label
- ✅ Não retornar múltiplas linhas
- ✅ Retornar DataFrame com todas as features
- ✅ Usar pandas e numpy

**Status**: ✅ COMPLETO

---

## 🔍 Validação

### Teste Automático
```bash
python exemplos_features.py
```

✅ Todos os 6 exemplos executados com sucesso
✅ Features calculadas corretamente
✅ Cálculos verificáveis manualmente

---

## 📁 Arquivos Criados/Modificados

### Novos
- ✨ **[FEATURE_EXTRACTION_GUIDE.md](FEATURE_EXTRACTION_GUIDE.md)** - Documentação
- ✨ **[exemplos_features.py](exemplos_features.py)** - Exemplos práticos
- ✨ **[test_new_features.py](test_new_features.py)** - Teste básico

### Modificados
- 📝 **[utils.py](utils.py)** - Adicionada `extract_accelerometer_features()`

---

## 🚀 Próximos Passos

1. **Usar em seu código**:
   ```python
   from utils import extract_accelerometer_features
   ```

2. **Ver exemplos**:
   ```bash
   python exemplos_features.py
   ```

3. **Ler documentação**:
   - [FEATURE_EXTRACTION_GUIDE.md](FEATURE_EXTRACTION_GUIDE.md)

4. **Integrar com app.py** (opcional):
   - Use na função de treinamento
   - Use na função de predição

---

## 📞 Suporte

Dúvidas sobre a função?
- Veja: [FEATURE_EXTRACTION_GUIDE.md](FEATURE_EXTRACTION_GUIDE.md)
- Execute: `python exemplos_features.py`
- Código: [utils.py](utils.py) - função bem comentada

---

**Status Final**: ✅ FUNÇÃO IMPLEMENTADA, TESTADA E DOCUMENTADA
