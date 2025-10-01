import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch 

# Mock da função process_email (IA)
@pytest.fixture(autouse=True)
def mock_process_email(monkeypatch):
    def fake_process_email(texto):
        return {
            "categoria": "Produtivo",
            "resposta_sugerida": "Mensagem de teste processada com sucesso."
        }
    monkeypatch.setattr("email_classifier.views.process_email", fake_process_email)

#Teste GET
@pytest.mark.django_db
def test_index_get(client):
    url = reverse("index")  
    response = client.get(url)
    assert response.status_code == 200
    # Verifica que o contexto padrão é None ou uma string vazia (antes da análise)
    assert response.context["categoria"] is None or response.context["categoria"] == "" 

#Teste POST com texto
@pytest.mark.django_db
def test_index_post_texto(client):
    url = reverse("index")
    data = {"content": "Preciso saber o status da minha fatura."}
    response = client.post(url, data)
    assert response.status_code == 200
    context = response.context
    # O mock retorna Produtivo, então deve ser Produtivo
    assert context["categoria"] == "Produtivo" 
    assert "Mensagem de teste" in context["resposta"]


# Teste de Uploads (Usando Mock na função read_uploaded_file)
@pytest.mark.django_db
@patch("email_classifier.views.read_uploaded_file", return_value="Conteúdo simulado do arquivo TXT.")
def test_index_post_txt_file(mock_read_file, client):
    url = reverse("index")
    # Apenas simula o objeto de arquivo
    file_mock = SimpleUploadedFile("teste.txt", b"arquivo de teste", content_type="text/plain")
    
    response = client.post(url, {"file": file_mock})
    assert response.status_code == 200
    context = response.context
    
    # Verifica se a função auxiliar de leitura foi chamada
    mock_read_file.assert_called_once() 
    
    assert context["categoria"] == "Produtivo"
    assert "Mensagem de teste" in context["resposta"]


# ATENÇÃO: Este teste sobrescreve o mock global, o retorno DEVE ser um DICIONÁRIO.
@pytest.mark.django_db
@patch("email_classifier.views.process_email")
@patch("email_classifier.views.read_uploaded_file", return_value="Conteúdo simulado do PDF.")
def test_index_post_existing_pdf_mocked(mock_read_file, mock_process, client):
    url = reverse("index")

    # Força retorno da IA como DICIONÁRIO (como o nlp.py deve retornar)
    mock_process.return_value = {"categoria": "Improdutivo", "resposta_sugerida": "Sem necessidade de resposta."}

    # Cria um mock de arquivo PDF
    pdf_mock = SimpleUploadedFile("Pdf_test.pdf", b"conteudo_pdf_fake", content_type="application/pdf")

    response = client.post(url, {"file": pdf_mock})
    context = response.context

    assert response.status_code == 200
    assert context["categoria"] == "Improdutivo"
    assert "Sem necessidade de resposta" in context["resposta"]

# --- 4. Testes de Erro e Limites ---

@pytest.mark.django_db
def test_index_post_arquivo_grande(client):
    url = reverse("index")
    # Cria o objeto de arquivo grande, definindo o atributo size
    big_file = SimpleUploadedFile("grande.txt", b"0" * (11 * 1024 * 1024), content_type="text/plain")
    
    response = client.post(url, {"file": big_file})
    assert response.status_code == 200
    context = response.context
    
    # A view deve abortar a classificação e retornar a mensagem de erro
    assert context["categoria"] is None or context["categoria"] == "" 
    assert "Arquivo muito grande" in context["resposta"]


@pytest.mark.django_db
def test_index_process_email_exception(client):
    """
    Testa se a View captura uma exceção e define a categoria/resposta de erro.
    """
    # força process_email a lançar uma exceção
    with patch("email_classifier.views.process_email", side_effect=Exception("Falha na IA")):
        response = client.post(reverse("index"), {"content": "texto de teste"})

    assert response.status_code == 200
    context = response.context
    
    # Verifica que a categoria é definida como ERRO (ou deve ser None, dependendo da sua correção)
    # Aqui, assumimos que se a categoria não é definida no 'except', ela fica None.
    # Se você corrigiu o views.py para context["categoria"] = "ERRO" no except, use "ERRO"
    assert context["categoria"] is None or context["categoria"] == "ERRO"
    assert "Erro ao processar a resposta da IA." in context["resposta"]