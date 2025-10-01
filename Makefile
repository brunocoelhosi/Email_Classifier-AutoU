# Makefile para Email Classifier AutoU

# Variáveis
VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
MANAGE := $(PYTHON) manage.py

# Default target
.DEFAULT_GOAL := help

# ------------------------------------------------
# Targets
# ------------------------------------------------

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup          - Configuração completa do projeto (venv, dependências, spaCy, NLTK, migrações)"
	@echo "  make venv           - Criar ambiente virtual"
	@echo "  make install        - Instalar dependências do requirements.txt"
	@echo "  make spacy          - Baixar modelo spaCy pt_core_news_sm"
	@echo "  make nltk           - Baixar stopwords do NLTK"
	@echo "  make migrate        - Aplicar migrações do Django"
	@echo "  make run            - Rodar servidor Django"
	@echo "  make test           - Rodar testes com pytest"
	@echo "  make coverage       - Rodar testes com pytest e gerar cobertura"
	@echo "  make docker-up      - Subir containers Docker"
	@echo "  make docker-down    - Parar e remover containers Docker"

# ------------------------------------------------
# Configuração completa
# ------------------------------------------------
setup: venv install spacy nltk migrate
	@echo "Setup concluído! Você pode rodar 'make run' para iniciar o servidor."

# ------------------------------------------------
# Criar ambiente virtual
# ------------------------------------------------
venv:
	python3 -m venv $(VENV_DIR)
	@echo "Ambiente virtual criado em $(VENV_DIR)."
	@echo "Ative com: source $(VENV_DIR)/bin/activate"

# ------------------------------------------------
# Instalar dependências
# ------------------------------------------------
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ------------------------------------------------
# Baixar modelo spaCy
# ------------------------------------------------
spacy: venv
	$(PYTHON) -m spacy download pt_core_news_sm

# ------------------------------------------------
# Baixar stopwords NLTK
# ------------------------------------------------
nltk: venv
	$(PYTHON) -m nltk.downloader stopwords

# ------------------------------------------------
# Aplicar migrações
# ------------------------------------------------
migrate:
	$(MANAGE) migrate

# ------------------------------------------------
# Rodar servidor Django
# ------------------------------------------------
run:
	$(MANAGE) runserver

# ------------------------------------------------
# Rodar testes
# ------------------------------------------------
test:
	$(PYTHON) -m pytest tests/

# ------------------------------------------------
# Rodar testes com cobertura
# ------------------------------------------------
coverage:
	$(PYTHON) -m pytest --cov=email_classifier --cov-report=html

# ------------------------------------------------
# Docker
# ------------------------------------------------
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
