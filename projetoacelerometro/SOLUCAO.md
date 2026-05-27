# Solução: Correção de Arquivos CSV sem Labels

## Problema Identificado

O sistema de machine learning estava falhando ao processar arquivos CSV que não tinham a coluna `label` ou cujos labels não eram detectáveis. Existem dois cenários:

1. **Arquivos para Treinamento (Train)**: Precisam obrigatoriamente de um label para cada amostra
2. **Arquivos para Predição (Predict)**: Não precisam de labels

## Arquivos Corrigidos

Todos os arquivos `teste_acelerometro.csv` que faltavam a coluna `label` foram corrigidos com o valor `"parado"`:

- ✅ 0775fdf6-a18d-40d6-acd3-8951ac22a122/teste_acelerometro.csv
- ✅ 256d469c-b240-4e80-9c20-ab3146399979/teste_acelerometro.csv
- ✅ 4710b624-b2bf-4c28-a173-4fbe9d5db3bf/teste_acelerometro.csv
- ✅ 56aed7f8-2dd1-4b43-90f1-3ab0f7af94c1/teste_acelerometro.csv
- ✅ 57005fe2-053f-4e4d-bf38-41a56716c278/teste_acelerometro.csv
- ✅ 6371834c-3e3d-4b43-8716-c725a90456c3/teste_acelerometro.csv
- ✅ c4aaac97-542c-46ce-a400-a0240f99e7d3/teste_acelerometro.csv
- ✅ dbcf01c9-ab47-4067-86b7-7755e3447c55/teste_acelerometro.csv
- ✅ e3a5bb9a-1b32-4b79-908c-10aa00446c64/teste_acelerometro.csv
- ✅ e9b23ead-3367-4530-8666-b05fa663820f/teste_acelerometro.csv

## Melhorias Implementadas

### 1. Script `add_labels.py`

Novo script utilitário para adicionar coluna `label` a arquivos CSV sem a necessidade de edição manual.

**Uso:**
```bash
# Adicionar label a um arquivo
python add_labels.py "caminho/arquivo.csv" "label_value"

# Adicionar labels a múltiplos arquivos
python add_labels.py \
  "arquivo1.csv" "label1" \
  "arquivo2.csv" "label2" \
  "arquivo3.csv" "label3"
```

**Exemplo:**
```bash
python add_labels.py "uploads/38b87887-ba40-4104-aa6f-c1aba74c4477/teste_acelerometro.csv" "parado"
```

### 2. Detecção de Labels Melhorada (utils.py)

A função `load_file_as_array()` foi aprimorada para:
- Reconhecer colunas `x, y, z` (original)
- Reconhecer colunas `ax, ay, az` (novo) ✨
- Ignorar a coluna `label` ao selecionar as 3 primeiras colunas numéricas

### 3. Detecção de Labels Robusta (app.py)

Nova função `detect_label_from_file()` que tenta 4 estratégias para detectar labels:

1. **Labels Map**: Arquivo `labels.csv` ou `labels.json` dentro de um ZIP
2. **Coluna Label**: Coluna `label` no próprio arquivo CSV
3. **Nome do Arquivo**: Prefixo antes do primeiro underscore (ex: `parado_001.csv` → `parado`)
4. **Nome da Pasta**: Se a pasta contiver um nome significativo (não UUID)

## Formato de Arquivo Esperado

### Arquivos para Treinamento (Obrigatório ter labels)

```csv
x,y,z,label
0.05,0.02,9.79,parado
-0.03,-0.04,9.83,parado
0.01,0.00,9.78,parado
```

Ou com nomes alternativos de colunas:

```csv
ax,ay,az,label
0.05,0.02,9.79,walking
-0.03,-0.04,9.83,running
0.01,0.00,9.78,standing
```

### Alternativa: Arquivo com Labels Separado (labels.csv)

Coloque um arquivo `labels.csv` dentro de um ZIP junto com os dados:

```csv
filename,label
data1.csv,walking
data2.csv,running
data3.csv,standing
```

## Próximos Passos

Se você receber novamente o arquivo de diagnóstico (`*_train_diagnostic.csv`), significa que há arquivos sem labels detectáveis. Você pode:

1. **Adicionar labels manualmente** ao arquivo CSV:
   - Abra o arquivo em um editor (Excel, Notepad, etc)
   - Adicione uma coluna chamada `label`
   - Preecha com o valor apropriado para cada linha

2. **Usar o script `add_labels.py`**:
   ```bash
   python add_labels.py "seu_arquivo.csv" "seu_label"
   ```

3. **Usar um arquivo `labels.csv` em um ZIP**:
   - Crie um arquivo `labels.csv` com mapeamento de arquivos → labels
   - Coloque tudo em um ZIP
   - Upload do ZIP

## Exemplo Prático

Se você tem um novo arquivo `novo_teste.csv` sem label, pode corrigir assim:

```bash
python add_labels.py "uploads/seu_id/novo_teste.csv" "parado"
```

Depois, pode fazer upload novamente ou usar para treinamento/predição.
