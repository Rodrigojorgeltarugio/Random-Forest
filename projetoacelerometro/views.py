from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import pandas as pd

from .ml_models import extract_features


@require_http_methods(["GET", "POST"])
def extract_features_view(request):
    """View Django para receber um CSV via POST e retornar tabela HTML com features.

    - Espera arquivo em campo 'file' (form enctype="multipart/form-data")
    - Em caso de erro, retorna mensagem amigável no template
    """
    result_html = ""
    if request.method == 'POST':
        uploaded = request.FILES.get('file')
        if not uploaded:
            result_html = '<div class="alert alert-warning">Nenhum arquivo enviado.</div>'
            return render(request, 'result.html', {'result': result_html, 'links': []})

        # Enforce single-file upload: reject if more than one file sent
        uploaded_list = request.FILES.getlist('file')
        if len(uploaded_list) == 0:
            result_html = '<div class="alert alert-warning">Nenhum arquivo enviado.</div>'
            return render(request, 'result.html', {'result': result_html, 'links': []})
        if len(uploaded_list) > 1:
            result_html = '<div class="alert alert-warning">Envie apenas um arquivo por vez.</div>'
            return render(request, 'result.html', {'result': result_html, 'links': []})

        # use the single uploaded file
        uploaded = uploaded_list[0]

        # Tentar ler o CSV com diferentes encodings comuns para evitar erros de upload
        df = None
        read_errors = []
        for enc in (None, 'utf-8', 'latin1'):
            try:
                if enc is None:
                    df = pd.read_csv(uploaded)
                else:
                    # reset file pointer
                    uploaded.seek(0)
                    df = pd.read_csv(uploaded, encoding=enc)
                break
            except Exception as e:
                read_errors.append((enc, str(e)))

        if df is None:
            msg = 'Não foi possível ler o arquivo CSV enviado. Tente salvar como UTF-8 ou Latin-1 e envie novamente.'
            details = ' | '.join([f"enc={e[0]}: {e[1]}" for e in read_errors])
            result_html = f'<div class="alert alert-danger">{msg} <small>{details}</small></div>'
            return render(request, 'result.html', {'result': result_html, 'links': []})

        try:
            features_df = extract_features(df)
            html = features_df.to_html(classes='table table-striped table-bordered table-sm', index=False, justify='center')
            result_html = html
        except ValueError as ve:
            # Erro previsto de validação (colunas faltando ou não numéricas)
            result_html = f'<div class="alert alert-warning">{str(ve)}</div>'
        except Exception as e:
            # mensagem amigável para outros erros
            msg = 'Ocorreu um erro ao extrair features. Verifique o arquivo e tente novamente.'
            detail = str(e)
            result_html = f'<div class="alert alert-danger">{msg} <small>{detail}</small></div>'

    return render(request, 'result.html', {'result': result_html, 'links': []})
