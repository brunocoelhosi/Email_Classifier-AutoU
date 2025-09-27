# classifier/api.py
from ninja import Router
from .schemas import EmailInput, ClassificationOutput

router = Router()

def processar_email_com_llm(email_content: str) -> dict:
    # 1. Montar o prompt conforme o exemplo na seção 1.A.
    # 2. Chamar o LLM (ex: client.chat.completions.create(...) com prompt e response_format={"type": "json_object"})
    
    # SIMULAÇÃO:
    if "status" in email_content.lower() or "dúvida" in email_content.lower():
        categoria = "Produtivo"
        resposta = "Obrigado por seu e-mail. Por favor, forneça o número de protocolo ou mais detalhes para que possamos verificar o status de sua requisição. Nossa equipe de suporte retornará em até 24h."
    else:
        categoria = "Improdutivo"
        resposta = "Obrigado pela sua mensagem! Agradecemos o contato e desejamos um excelente dia."
        
    return {"categoria": categoria, "resposta_sugerida": resposta}


@router.post("/classificar_email", response=ClassificationOutput)
def classify_email(request, data: EmailInput):
    # Chama a função que interage com o Google Gemini ou OpenAI
    resultado_llm = processar_email_com_llm(data.email_text)

    return resultado_llm