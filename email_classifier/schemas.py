from ninja import Schema

class EmailInput(Schema):
    email_text: str

class ClassificationOutput(Schema):
    categoria: str
    resposta_sugerida: str