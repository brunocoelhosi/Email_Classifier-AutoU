import io
import json
import pytest
from django.urls import reverse

# Mock da função process_email para não chamar a IA nos testes
@pytest.fixture(autouse=True)
def mock_process_email(monkeypatch):
    def fake_process_email(texto):
        return json.dumps({
            "categoria": "Produtivo",
            "resposta_sugerida": "Mensagem de teste processada com sucesso."
        })
    monkeypatch.setattr("email_classifier.views.process_email", fake_process_email)


@pytest.mark.django_db
def test_index_get(client):
    url = reverse("index")  # precisa estar configurado no urls.py
    response = client.get(url)
    assert response.status_code == 200
    assert b"categoria" not in response.content  # não deve ter classificação ainda


@pytest.mark.django_db
def test_index_post_texto(client):
    url = reverse("index")
    data = {"content": "Preciso saber o status da minha fatura."}
    response = client.post(url, data)
    assert response.status_code == 200
    context = response.context
    assert context["categoria"] == "Produtivo"
    assert "Mensagem de teste" in context["resposta"]


@pytest.mark.django_db
def test_index_post_txt_file(client):
    url = reverse("index")
    file_content = io.BytesIO(b"Email de teste em arquivo txt")
    file_content.name = "teste.txt"
    response = client.post(url, {"file": file_content})
    assert response.status_code == 200
    context = response.context
    assert context["categoria"] == "Produtivo"
    assert "Mensagem de teste" in context["resposta"]


"""@pytest.mark.django_db
def test_index_post_pdf_file(client):
    url = reverse("index")
    # Criando um PDF de teste simples
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Conteúdo de teste PDF")
    c.save()
    pdf_buffer.seek(0)
    pdf_buffer.name = "teste.pdf"

    response = client.post(url, {"file": pdf_buffer})
    assert response.status_code == 200
    context = response.context
    assert context["categoria"] == "Produtivo"

"""
@pytest.mark.django_db
def test_index_post_arquivo_grande(client):
    url = reverse("index")
    big_file = io.BytesIO(b"0" * (11 * 1024 * 1024))  # 11MB
    big_file.name = "grande.txt"

    response = client.post(url, {"file": big_file})
    assert response.status_code == 200
    context = response.context
    assert "Arquivo muito grande" in context["resposta"]
