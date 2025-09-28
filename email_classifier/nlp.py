# app/nlp.py
import re
import nltk
from transformers import pipeline

# Baixar recursos necessários do NLTK
nltk.download("stopwords")
from nltk.corpus import stopwords

stop_words = set(stopwords.words("portuguese"))

classifier = pipeline("text-classification", model="pierreguillou/bert-base-cased-sentiment-br")
generator = pipeline("text-generation", model="pierreguillou/gpt2-small-portuguese")

def preprocess(text: str) -> str:
    text = re.sub(r"\W+", " ", text.lower())
    tokens = [w for w in text.split() if w not in stop_words]
    return " ".join(tokens)

def process_email(content: str) -> dict:
    cleaned = preprocess(content)

    # Classificação
    classification = classifier(cleaned[:512])[0]
    categoria = "Produtivo" if classification["label"] == "POS" else "Improdutivo"

    # Resposta automática
    if categoria == "Produtivo":
        resposta = generator("Obrigado pelo seu contato, vamos analisar com atenção:")[0]["generated_text"]
    else:
        resposta = generator("Agradecemos, mas essa mensagem não se enquadra como produtiva.")[0]["generated_text"]

    return {"categoria": categoria, "resposta": resposta}
