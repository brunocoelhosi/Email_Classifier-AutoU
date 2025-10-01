from django.shortcuts import render
from .nlp import process_email 
from .utils import read_uploaded_file 
from .logger import logger

# Limite de upload em bytes (10 MB)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  

def index(request):
    categoria = resposta = conteudo = None
    
    # Prepara o contexto padrão para manter o estado do formulário
    context = {
        "categoria": None,
        "resposta": None,
        "conteudo": request.POST.get("content", "")
    }

    if request.method == "POST":
        conteudo_texto = request.POST.get("content", "").strip()
        conteudo_arquivo = ""

        uploaded_file = request.FILES.get("file")
        
        # Tratamento do arquivo enviado
        if uploaded_file:

            logger.info(f"Arquivo recebido: {uploaded_file.name}, Tamanho: {uploaded_file.size} bytes.") # Arquivo recebido
            
            if uploaded_file.size > MAX_UPLOAD_SIZE:
                context["resposta"] = f"Arquivo muito grande ({uploaded_file.size/1024/1024:.2f} MB). O limite é 10MB."
                logger.warning(f"Rejeitado arquivo por tamanho: {uploaded_file.name}") # Aviso de arquivo grande
            else:
                # Chama a função para fazer a leitura (TXT/PDF)
                conteudo_arquivo = read_uploaded_file(uploaded_file)
                logger.info("Leitura do arquivo concluída.") # Leitura concluída
                
        # Concatena o conteúdo (texto + arquivo)
        conteudo = "\n".join([c for c in [conteudo_texto, conteudo_arquivo] if c])
        
        # Chama o serviço de processamento se houver conteúdo
        if conteudo and not context["resposta"]:
            try:
                logger.info("Chamando nlp.process_email...") # Antes da chamada da IA
                resultado_dict = process_email(conteudo) 
                logger.info(f"Classificação recebida: {resultado_dict.get('categoria')}") # Sucesso na classificação
                
                # Atualiza o contexto com os resultados
                context["categoria"] = resultado_dict.get("categoria", "ERRO")
                context["resposta"] = resultado_dict.get("resposta_sugerida", "Erro de serviço interno.")
                
            except Exception as e:
                logger.error(f"Erro fatal no processamento da IA: {e}", exc_info=True) 
                context["resposta"] = "Erro ao processar a resposta da IA."

    return render(request, "index.html", context)