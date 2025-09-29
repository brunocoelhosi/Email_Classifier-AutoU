from ninja import Router
from typing import Dict
from .nlp import process_email

router = Router()

@router.post("/processar_email")
def processar_email(request, email: str):
    resultado = process_email(email)
    return {"resultado": resultado}