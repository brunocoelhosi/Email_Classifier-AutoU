from django.shortcuts import render
from .nlp import process_email
import json
from pypdf import PdfReader  # substitui PyPDF2

# limite de upload em bytes (10 MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  

def index(request):
    categoria = resposta = conteudo = None

    if request.method == "POST":
        conteudo_texto = request.POST.get("content", "").strip()
        conteudo_arquivo = ""

        uploaded_file = request.FILES.get("file")
        if uploaded_file:
            print("Arquivo recebido:", uploaded_file.name, "Tamanho:", uploaded_file.size)

            if uploaded_file.size > MAX_UPLOAD_SIZE:
                resposta = f"Arquivo muito grande ({uploaded_file.size/1024/1024:.2f} MB). O limite é 10MB."
            else:
                if uploaded_file.name.endswith(".txt"):
                    # leitura em chunks para evitar carregar tudo em memória de uma vez
                    for chunk in uploaded_file.chunks():
                        conteudo_arquivo += chunk.decode("utf-8", errors="ignore")

                elif uploaded_file.name.endswith(".pdf"):
                    # reposiciona o ponteiro antes de passar para o PdfReader
                    uploaded_file.seek(0)
                    pdf_reader = PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        conteudo_arquivo += page.extract_text() or ""

        # Concatena o conteúdo do campo de texto e do arquivo
        conteudo = "\n".join([c for c in [conteudo_texto, conteudo_arquivo] if c])

        if conteudo:
            try:
                resultado = process_email(conteudo)
                resultado_json = json.loads(resultado)
                categoria = resultado_json.get("categoria", "")
                resposta = resultado_json.get("resposta_sugerida", "")
            except Exception as e:
                print("Erro no processamento:", e)
                resposta = "Erro ao interpretar a resposta da IA."

    context = {
        "categoria": categoria,
        "resposta": resposta,
        "conteudo": request.POST.get("content", "")  # mantém o texto no form
    }

    return render(request, "index.html", context)
