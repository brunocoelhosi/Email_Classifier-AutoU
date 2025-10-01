import pytest
from django.test import TestCase
from ninja.testing import TestClient
from email_classifier.api import processar_email
from ninja import Router

test_router = Router()
test_router.add_api_operation(
    "/processar_email",
    ["POST"],
    processar_email,
)

class TestEmailAPI(TestCase):
    def setUp(self):
        self.client = TestClient(test_router)

    def test_processar_email_mockado(self):
        payload = {
            "email": "Olá, gostaria de informações sobre seus serviços."
        }

        response = self.client.post("/processar_email", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "categoria" in data
        assert "resposta_sugerida" in data
        assert data["categoria"] in ["Produtivo", "Improdutivo"]
