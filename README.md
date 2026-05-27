# Processador Automático de Dados de Acelerômetro

Este projeto fornece um site simples (Flask) para processar arquivos de acelerômetro. Funcionalidades:

- Upload de múltiplos arquivos (`CSV`, `JSON`, `NPY`, `XLSX`, `ZIP`).
- Tarefas: `Extrair features`, `Treinar modelo` (Random Forest) e `Prever`.
- Downloads diretos: arquivo CSV de features, arquivo CSV de predições, ou modelo treinado (`.joblib`).

Como usar

1. Instale dependências (crie e ative um virtualenv se desejar):

```powershell
python -m pip install -r requirements.txt
```

2. Rode o servidor:

```powershell
python app.py
```

3. Abra o navegador em `http://127.0.0.1:5000/` e submeta arquivos.

Notas sobre rotulagem para treino

- Para treinar, cada arquivo enviado deve ter um rótulo. O sistema tenta obter o rótulo de (na ordem):
  - coluna `label` em um arquivo CSV; ou
  - prefixo do nome do arquivo antes do primeiro underscore (`label_filename.csv`).

Se não houver rótulos suficientes, o treino falhará com mensagem apropriada.

Extensões possíveis

- Melhor UI com progresso/filas; usar Celery para trabalhos longos.
- Suporte a pastas organizadas por classe dentro de um ZIP para montar dataset automaticamente.
