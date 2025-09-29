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
    text = " ".join(text.split())
    doc = nlp_spacy(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def process_email(email_text: str):
    # Pré-processamento do texto
    preprocessed_text = preprocess_text(email_text)
    print(f"Texto pré-processado: {preprocessed_text}")

    prompt = f"""
    Você é um classificador de emails.
    Analise o email abaixo e responda **exatamente** no formato JSON:

    {{
      "categoria": "Produtivo" ou "Improdutivo",
      "resposta_sugerida": "Mensagem curta, educada e adequada ao remetente"
    }}

    Critérios:
    - "Produtivo": emails que pedem ação, suporte, informação ou resolução de problema.
    - "Improdutivo": emails informativos, convites, spam, propagandas ou mensagens sem necessidade de resposta.

    Email recebido (pré-processado):
    {preprocessed_text}
    """

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

