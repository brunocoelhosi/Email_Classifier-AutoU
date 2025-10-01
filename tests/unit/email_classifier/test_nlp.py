import pytest
from unittest.mock import patch, MagicMock
from email_classifier.nlp import preprocess_text, process_email
import json

# --- Testes de Pré-Processamento ---

def test_preprocess_text_remove_espacos_minusculas():
    texto = "   Olá,    Mundo!   "
    resultado = preprocess_text(texto)
    # Deve remover espaços extras e pontuação
    assert "olá" in resultado and "mundo" in resultado
    assert "  " not in resultado  # Não deve ter espaços duplos
    assert resultado.startswith("olá") # Verifica que espaços no início foram removidos


def test_preprocess_text_lematizacao():
    # O spaCy lematiza "correndo" para "correr" e "estavam" para "estar"
    texto = "os meninos estavam correndo rapidamente"
    resultado = preprocess_text(texto)
    assert "estar" in resultado
    assert "correr" in resultado
    # Garante que stop words e advérbios podem ser removidos (se seu nlp_spacy fizer isso)


# --- Testes de Serviço (process_email) ---

@patch("email_classifier.nlp.client")
@patch("email_classifier.nlp.preprocess_text", return_value="texto pre processado")
def test_process_email_mock_openai(mock_preprocess, mock_client):
    # Resposta que a API da OpenAI RETORNA (string JSON)
    json_string = '{"categoria": "Produtivo", "resposta_sugerida": "Ok, já estamos verificando."}'
    
    fake_response = MagicMock()
    # Mocka o conteúdo retornado pela API
    fake_response.choices = [MagicMock(message=MagicMock(content=json_string))]

    # Configura mock do cliente OpenAI
    mock_client.chat.completions.create.return_value = fake_response

    email = "Preciso de ajuda com minha conta, não consigo acessar."
    resultado = process_email(email)

    # O resultado deve ser um DICIONÁRIO
    assert isinstance(resultado, dict)
    assert resultado.get("categoria") == "Produtivo"
    assert resultado.get("resposta_sugerida") == "Ok, já estamos verificando."
    
    # Verifica se a chamada foi feita com o parâmetro JSON format
    args, kwargs = mock_client.chat.completions.create.call_args
    assert kwargs.get("response_format", {}).get("type") == "json_object"
    
    mock_client.chat.completions.create.assert_called_once()

@patch("email_classifier.nlp.client")
@patch("email_classifier.nlp.preprocess_text", return_value="texto pre processado")
def test_process_email_json_decode_error(mock_preprocess, mock_client):
    """ Testa o tratamento de erro se a IA retornar um JSON inválido. """
    
    # Resposta FAKE da API (String INVÁLIDA)
    invalid_string = '{"categoria": "Produtivo", "resposta_sugerida": "Ok, já estamos verificando."' 
    
    fake_response = MagicMock()
    fake_response.choices = [MagicMock(message=MagicMock(content=invalid_string))]
    mock_client.chat.completions.create.return_value = fake_response

    email = "email"
    resultado = process_email(email)

    # O resultado deve ser um DICIONÁRIO de ERRO seguro
    assert isinstance(resultado, dict)
    assert resultado.get("categoria") == "ERRO"
    assert "JSON" in resultado.get("resposta_sugerida")