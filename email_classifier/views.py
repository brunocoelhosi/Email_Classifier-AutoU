from django.shortcuts import render
from .nlp import process_email
import json
import PyPDF2

def index(request):
    categoria = resposta = conteudo = None

    if request.method == "POST":
        conteudo_texto = request.POST.get("content", "").strip()
        conteudo_arquivo = ""

        uploaded_file = request.FILES.get("file")
        if uploaded_file:
            if uploaded_file.name.endswith(".txt"):
                conteudo_arquivo = uploaded_file.read().decode("utf-8")
            elif uploaded_file.name.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    conteudo_arquivo += page.extract_text() or ""

        # Contatena o conteúdo do texto e do arquivo
        conteudo = "\n".join([c for c in [conteudo_texto, conteudo_arquivo] if c])

        if conteudo:
            resultado = process_email(conteudo)
            try:
                resultado_json = json.loads(resultado)
                categoria = resultado_json.get("categoria", "")
                resposta = resultado_json.get("resposta_sugerida", "")
            except Exception:
                resposta = "Erro ao interpretar a resposta da IA."

    context = {
        "categoria": categoria,
        "resposta": resposta,
        "conteudo": request.POST.get("content", "")  # mantém o texto no form
    }

    return render(request, "index.html", context)

