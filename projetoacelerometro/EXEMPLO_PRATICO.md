# EXEMPLO PRÁTICO - Como Usar o Sistema Corrigido

## Cenário 1: Você tem um arquivo sem label e quer adicionar

### Arquivo original: `dados.csv`
```csv
x,y,z
0.05,0.02,9.79
-0.03,-0.04,9.83
0.01,0.00,9.78
```

### ❌ Problema
Se você fizer upload deste arquivo para TREINAMENTO, o sistema vai rejeitar porque não tem `label`.

### ✅ Solução - Usar add_labels.py

**Passo 1**: Copie seu arquivo para o diretório do projeto

**Passo 2**: Execute o comando
```bash
python add_labels.py "dados.csv" "parado"
```

**Passo 3**: Arquivo corrigido: `dados.csv`
```csv
x,y,z,label
0.05,0.02,9.79,parado
-0.03,-0.04,9.83,parado
0.01,0.00,9.78,parado
```

### ✅ Agora funciona!
Upload para TREINAMENTO vai funcionar perfeitamente.

---

## Cenário 2: Você tem múltiplos arquivos com labels diferentes

### Arquivos originais
- `dados_parado.csv` (sem label)
- `dados_correndo.csv` (sem label)  
- `dados_andando.csv` (sem label)

### ✅ Corrigir todos de uma vez
```bash
python add_labels.py \
  "dados_parado.csv" "parado" \
  "dados_correndo.csv" "correndo" \
  "dados_andando.csv" "andando"
```

### ✅ Resultado
Todos os arquivos agora têm a coluna `label` com seus valores correspondentes!

---

## Cenário 3: Você quer verificar se o sistema está OK

### Execute o teste de validação
```bash
python test_validation.py
```

### Resultado esperado
```
TESTE DE VALIDACAO - Arquivos CSV Corrigidos
====================================
Arquivo: teste_acelerometro.csv
  [OK] Label detectado: 'parado'
  [OK] Array carregado: 10 amostras x 3 features
  [OK] Features extraidas: 33 features
...
====================================
[OK] Teste aprovado! O sistema esta pronto para treinamento.
```

---

## Cenário 4: Você quer fazer um upload para TREINAMENTO

### Preparação
```bash
# 1. Seu arquivo sem label
python add_labels.py "meu_arquivo.csv" "parado"

# 2. Verificar se está tudo OK
python test_validation.py

# 3. Fazer upload via interface web
# - Selecione tarefa: "train"
# - Upload do arquivo corrigido
# - Clique em processar
```

### Resultado
✅ Modelo treinado com sucesso!

---

## Cenário 5: Detectar qual era o problema

Se você receber um arquivo de diagnóstico:

### Arquivo: `XXXXX_train_diagnostic.csv`
```csv
filename,detected_label
meu_arquivo.csv,NÃO DETECTADO
outro_arquivo.csv,parado
```

### Solução
```bash
# Corrigir os arquivos que não foram detectados
python add_labels.py "meu_arquivo.csv" "parado"

# Tentar novamente
python test_validation.py
```

---

## Referência Rápida - Comandos

### Adicionar label a arquivo
```bash
python add_labels.py "arquivo.csv" "label"
```

### Adicionar labels a múltiplos arquivos
```bash
python add_labels.py \
  "arquivo1.csv" "label1" \
  "arquivo2.csv" "label2" \
  "arquivo3.csv" "label3"
```

### Validar sistema
```bash
python test_validation.py
```

### Iniciar servidor
```bash
python app.py
```

---

## Dicas Importantes

### ✅ DO (Faça)
- Use nomes consistentes: `parado`, `correndo`, `andando`
- Verifique com `test_validation.py` antes de usar
- Use `add_labels.py` para correção rápida
- Mantenha arquivos com pelo menos 2-3 labels diferentes para treinar

### ❌ DON'T (Evite)
- Não misture nomes de labels: `parado` vs `Parado` vs `PARADO`
- Não deixe linhas com label vazio
- Não misture formatos: `x,y,z` com `ax,ay,az`

---

## Exemplo Completo End-to-End

```bash
# 1. Você tem um arquivo sem label
# Arquivo: "dados.csv" (apenas x, y, z)

# 2. Adicionar label
python add_labels.py "dados.csv" "parado"

# 3. Validar
python test_validation.py
[OK] Teste aprovado!

# 4. Fazer upload via web interface
# - Selecione arquivo corrigido
# - Selecione tarefa "train"
# - Aguarde resultado

# 5. ✅ Modelo treinado com sucesso!
```

---

## Estrutura Esperada Final

```
projetoacelerometro/
├── app.py
├── utils.py
├── add_labels.py              # NOVO ✨
├── test_validation.py         # NOVO ✨
├── SOLUCAO.md                 # NOVO ✨
├── RESUMO.md                  # NOVO ✨
├── RELATORIO_CORRECOES.md     # NOVO ✨
├── requirements.txt
├── uploads/
│   └── [seus arquivos corrigidos com labels]
├── outputs/
│   └── [modelos e resultados]
└── templates/
    ├── index.html
    └── result.html
```

---

**Próximo Passo**: Execute `python test_validation.py` para confirmar que tudo está funcionando!
