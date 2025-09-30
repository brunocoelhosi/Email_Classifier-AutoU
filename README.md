# 📧 Email Classifier AutoU 🤖

Este projeto é um **classificador automático de e-mails** que utiliza técnicas de Processamento de Linguagem Natural (NLP) e Inteligência Artificial para categorizar e sugerir respostas automáticas para e-mails recebidos. O backend é desenvolvido em Python com Django e integra modelos de IA via API (OpenAI). A interface web permite ao usuário o upload de arquivos de email em formatos .txt ou .pdf ou a inserção direta de texto e receber a classificação e sugestão de resposta.

---

## 📚 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Pré-requisitos](#️-pré-requisitos)
- [⚙️ Instalação](#️-instalação)
- [🔧 Configuração do Ambiente](#-configuração-do-ambiente)
- [🚀 Como Usar](#-como-usar)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧰 Principais Tecnologias](#-principais-tecnologias)
- [📝 Notas sobre NLP](#-notas-sobre-nlp)
- [🎨 Personalização](#-personalização)
- [📝 Licença](#-licença)

---

## ✨ Funcionalidades

- 🤖 **Classificação automática** de e-mails em "Produtivo" ou "Improdutivo"
- 💬 **Sugestão automática de resposta** baseada na categoria identificada
- 🧹 **Pré-processamento de texto** com técnicas de NLP (minúsculas, remoção de espaços, lemmatização, remoção de stopwords)
- 🖥️ **Interface web** fluída para interação
- 🔗 **Integração com API de IA** (OpenAI GPT)

---

## 🛠️ Pré-requisitos

- 🐍 Python 3.10+
- 📦 [pip](https://pip.pypa.io/en/stable/)
- 🛡️ [virtualenv](https://virtualenv.pypa.io/en/latest/)
- 🔑 Conta e chave de API da [OpenAI](https://platform.openai.com/)

---

## ⚙️ Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/Email_Classifier-AutoU.git
   cd Email_Classifier-AutoU
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Instale o modelo spaCy para português:**

   ```bash
   python -m spacy download pt_core_news_sm
   ```

5. **Baixe recursos do NLTK se for usar:**
   ```bash
   python -m nltk.downloader stopwords
   ```

---

## 🔧 Configuração do Ambiente

1. **Crie um arquivo `.env` na raiz do projeto com sua chave da OpenAI:**

   ```
   OPENAI_API_KEY=sua-chave-aqui
   ```

2. **Configure o Django (se necessário):**
   - Ajuste `settings.py` para incluir `'email_classifier'` em `INSTALLED_APPS`.
   - Configure os diretórios `STATICFILES_DIRS` e `TEMPLATES` conforme necessário.

---

## 🚀 Como Usar

1. **Execute as migrações do Django:**

   ```bash
   python manage.py migrate
   ```

2. **Inicie o servidor de desenvolvimento:**

   ```bash
   python manage.py runserver
   ```

3. **Acesse a interface web:**

   - Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador.

4. **Utilize a API Ninja (Swagger):**
   - Acesse [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs) para testar a API.

---

## 📁 Estrutura do Projeto

```
email_classifier/
├── __init__.py
├── admin.py
├── api.py           # Rotas da API Ninja
├── apps.py
├── models.py
├── nlp.py           # Funções de NLP e integração com OpenAI
├── schemas.py
├── tests.py
├── views.py         # Views Django para interface web
├── migrations/
│   └── ...
├── static/
│   └── css/
│       └── style.css
└── templates/
    └── index.html
```

---

## 🧰 Principais Tecnologias

- 🐍 **Python** & **Django**: Backend e servidor web
- ⚡ **Django Ninja**: Criação de APIs rápidas e documentação automática
- 🤖 **OpenAI GPT**: Classificação e sugestão de resposta via IA
- 🧠 **spaCy**: Pré-processamento de texto (lemmatização, stopwords, etc.)
- 🎨 **HTML/CSS**: Interface web

---

## 📝 Notas sobre NLP

O pré-processamento do texto inclui:

- 🔡 Conversão para minúsculas
- 🧹 Remoção de espaços em branco extras
- 🪄 Lematização (redução das palavras à sua forma base)
- 🚫 Remoção de stopwords e pontuação

Essas etapas são realizadas antes de enviar o texto para a IA, tornando a análise mais eficiente e precisa.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
