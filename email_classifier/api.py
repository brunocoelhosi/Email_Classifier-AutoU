from ninja import Router
from .nlp import process_email
from .schemas import EmailInput, ClassificationOutput
from .logger import logger
from ninja.errors import HttpError

router = Router()

@router.post("/processar_email",
            response = ClassificationOutput,
            summary="Classifica e gera resposta para o e-mail",
            description="""
                Recebe um e-mail e retorna:

                1. **Categoria do e-mail** (`categoria`):
                - `"Produtivo"`: Emails que requerem ação, solicitação de informação, suporte ou atualização.
                - `"Improdutivo"`: Emails informativos, agradecimentos, felicitações ou spam.

                2. **Resposta sugerida** (`resposta_sugerida`):
                - Uma mensagem curta, educada e adequada para responder ao remetente.

                **Exemplo de input:**
                {
                    "email": "Olá, estou interessado em adquirir seus serviços financeiros. Poderiam me enviar mais informações?"
                }

                **Exemplo de output:**
                {
                    "categoria": "Produtivo",
                    "resposta_sugerida": "Olá! Agradecemos seu interesse em nossos serviços financeiros. Enviaremos mais informações em breve."
                }

                """
)
def processar_email(request, payload:EmailInput):
    try:
        resultado = process_email(payload.email)
        # Verifica se a IA retornou erro
        if resultado.get("categoria") == "ERRO":
            raise HttpError(500, resultado["resposta_sugerida"])
        return ClassificationOutput(**resultado)
    
    except Exception as e:
        # Loga o erro
        logger.error(f"Erro no endpoint: {e}")
        raise HttpError(500, "Ocorreu um erro ao processar o e-mail.")