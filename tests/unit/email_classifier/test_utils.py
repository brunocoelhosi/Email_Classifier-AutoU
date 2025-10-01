from email_classifier.utils import read_uploaded_file
from unittest.mock import MagicMock, patch

def test_read_uploaded_file_txt():
    # Cria um mock de SimpleUploadedFile
    mock_file = MagicMock()
    mock_file.name = "teste.txt"
    # Simula o retorno de chunks
    mock_file.chunks.return_value = [b"Primeira linha.\n", b"Segunda linha."]

    content = read_uploaded_file(mock_file)
    assert "Primeira linha." in content
    assert "Segunda linha." in content

@patch("email_classifier.utils.PdfReader")
def test_read_uploaded_file_pdf(mock_pdf_reader):
    # Cria um mock de SimpleUploadedFile
    mock_file = MagicMock()
    mock_file.name = "documento.pdf"

    # Configura o mock do PdfReader para simular páginas
    mock_page1 = MagicMock()
    mock_page1.extract_text.return_value = "Texto da página um."
    mock_page2 = MagicMock()
    mock_page2.extract_text.return_value = "Texto da página dois."

    # Configura o mock do PdfReader para retornar essas páginas
    mock_pdf_reader.return_value.pages = [mock_page1, mock_page2]

    content = read_uploaded_file(mock_file)

    # Verifica que a seek foi chamada
    mock_file.seek.assert_called_once_with(0) 
    assert "Texto da página um." in content
    assert "Texto da página dois." in content