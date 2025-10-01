from openai import OpenAI
from dotenv import load_dotenv
import os
import spacy
import json
from .logger import logger_nlp as logger

# Carrega o modelo de NLP para português
nlp_spacy = spacy.load("pt_core_news_sm")

load_dotenv()  # carrega o .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preprocess_text(text: str) -> str:
    # Converte para minúsculas e remove espaços extras
    text = text.lower().strip()
    # Remove múltiplos espaços
    text = " ".join(text.split())
    # Processa o texto com spaCy
    doc = nlp_spacy(text)
    # Lematização e remoção de pontuação
    tokens = [token.lemma_ for token in doc if not token.is_punct]
    return " ".join(tokens)

def process_email(email_text: str) -> dict: # <--- Retorna um dicionário
    """
    Pré-processa o e-mail, envia para a OpenAI e retorna um dicionário Python.
    """
    # Pré-processa o texto do email
    logger.info(f"Texto ORIGINAL recebido (Tamanho: {len(email_text)} caracteres).")
    preprocessed_text = preprocess_text(email_text)

    logger.info(f"Texto pré-processado: {preprocessed_text}")

    # Cria o prompt para a API da OpenAI
    prompt = f"""
    Você é um classificador de emails de uma empresa do setor financeiro que recebe um alto volume de mensagens diariamente.
    Sua função é classificar cada email recebido e sugerir uma resposta curta e educada, **exatamente** no formato JSON abaixo:

    {{
    "categoria": "Produtivo" ou "Improdutivo",
    "resposta_sugerida": "Mensagem curta, educada e adequada ao remetente"
    }}

    Critérios:
    - "Produtivo": Emails que pedem ação, suporte, informação, resolução de problema, atualização sobre casos em aberto, envio de arquivos relevantes ou dúvidas sobre o sistema/serviços.
    - "Improdutivo": Emails informativos, felicitações, agradecimentos, convites, spam, propagandas ou mensagens sem necessidade de ação.

    Email recebido (pré-processado):
    {preprocessed_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} 
        )
        
        json_string = response.choices[0].message.content # Resposta da IA
        logger.info(f"Resposta JSON recebida: {json_string}")
        
        # Converte a string JSON em um dicionário Python
        resultado_dict = json.loads(json_string) 
        
        return resultado_dict # Retorna o dicionário
        
    except json.JSONDecodeError:
        # Erro se a resposta da IA não puder ser decodificada como JSON
        logger.error("Erro de decodificação JSON na resposta da IA.")
        return {"categoria": "ERRO", "resposta_sugerida": "Erro de decodificação JSON na resposta da IA."}
        
    except Exception as e:
        # Erro de conexão com a API ou outro
        logger.error(f"Erro na comunicação com a OpenAI: {e}")
        return {"categoria": "ERRO", "resposta_sugerida": "Erro na comunicação com o serviço de IA."}