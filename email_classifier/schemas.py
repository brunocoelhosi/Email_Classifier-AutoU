from ninja import Schema

class EmailInput(Schema):
    email: str

class ClassificationOutput(Schema):
    categoria: str
    resposta_sugerida: str