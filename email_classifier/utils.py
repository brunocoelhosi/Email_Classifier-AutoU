from pypdf import PdfReader
from .logger import logger

def read_uploaded_file(uploaded_file):
    """
    Lê o conteúdo de um arquivo (TXT ou PDF) carregado
    pelo Django (UploadedFile).
    """
    content = ""
    file_name = uploaded_file.name
    logger.info(f"Iniciando leitura de arquivo: {file_name}") # Início da leitura

    if file_name.endswith(".txt"):
        logger.info("Tipo de arquivo: TXT") # TXT identificado
        # Decodifica o TXT em chunks
        for chunk in uploaded_file.chunks():
            # 'errors="ignore"' trata caracteres inválidos
            content += chunk.decode("utf-8", errors="ignore")

    elif file_name.endswith(".pdf"):
        logger.info("Tipo de arquivo: PDF") # PDF identificado
        # Reposiciona o ponteiro para o início antes de ler o PDF
        uploaded_file.seek(0)
        
        try:
            pdf_reader = PdfReader(uploaded_file)
            logger.info(f"PDF possui {len(pdf_reader.pages)} páginas.") # NOVO: Detalhe do PDF
            for page in pdf_reader.pages:
                # Extrai o texto da página (pode ser None, por isso o 'or ""')
                content += page.extract_text() or ""
        except Exception as e:
            # Em caso de PDF corrompido ou protegido
            print(f"Erro ao ler PDF: {e}")
            logger.error(f"Erro ao ler PDF: {file_name}. Detalhe: {e}", exc_info=True) 
            return None 
    logger.info(f"Conteúdo do arquivo lido com sucesso. Tamanho: {len(content)}.") # NOVO: Fim com sucesso
    return content