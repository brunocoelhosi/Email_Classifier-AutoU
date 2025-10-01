from openai import OpenAI
from dotenv import load_dotenv
import os
import spacy

# Carrega o modelo de NLP para português
nlp_spacy = spacy.load("pt_core_news_sm")

load_dotenv()  # carrega o .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preprocess_text(text: str) -> str:
    # Converte para minúsculas e remove espaços extras
    text = text.lower().strip()
    # Remove múltiplos espaços
    text = " ".join(text.split())
    #
    doc = nlp_spacy(text)
    #
    tokens = [token.lemma_ for token in doc if not token.is_punct]
    return " ".join(tokens)

def process_email(email_text: str):

    # Pré-processa o texto do email
    preprocessed_text = preprocess_text(email_text)
    print(f"Texto pré-processado: {preprocessed_text}")

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

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
    )

    print(f"Texto processado: {response.choices[0].message.content}")

    return response.choices[0].message.content

