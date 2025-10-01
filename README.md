# 📧 Email Classifier AutoU 🤖

Este projeto é um **classificador automático de e-mails** que utiliza técnicas de Processamento de Linguagem Natural (NLP) e Inteligência Artificial para categorizar e sugerir respostas automáticas para e-mails recebidos.

O backend é desenvolvido em Python com Django e integra modelos de IA via API (OpenAI). A interface web permite ao usuário o upload de arquivos de email em formatos .txt ou .pdf ou a inserção direta de texto e receber a classificação e sugestão de resposta.

---

## 📚 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Pré-requisitos](#️-pré-requisitos)
- [🧰 Principais Tecnologias](#-principais-tecnologias)
- [📝 Notas sobre NLP](#-notas-sobre-nlp)
- [⚙️ Instalação](#️-instalação)
- [🔧 Configuração do Ambiente](#-configuração-do-ambiente)
- [🚀 Como Usar](#-como-usar)
- [🐳 Execução com Docker](#-execução-com-docker)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [📊 Cobertura de Código com pytest-cov](#-cobertura-de-código-com-pytest-cov)
- [📝 Licença](#-licença)

---

## ✨ Funcionalidades

- 🤖 **Classificação automática** de e-mails em "Produtivo" ou "Improdutivo"
- 💬 **Sugestão automática de resposta** baseada na categoria identificada
- 📝 **Processamento de arquivos**: Suporte para upload e leitura de conteúdo de arquivos **.txt** e **.pdf** (via `pypdf`).
- 🧹 **Pré-processamento de texto** com técnicas de NLP (minúsculas, remoção de espaços, lematização, remoção de stopwords)
- 🖥️ **Interface web** fluída para interação
- 🔗 **Integração com API de IA** (OpenAI GPT)
- 📢 **Sistema de Logging** robusto para monitoramento e diagnóstico de erros (Django, NLP, e API).

---

## 🛠️ Pré-requisitos

- 🐍 Python 3.10+
- 📦 [pip](https://pip.pypa.io/en/stable/)
- 🛡️ [virtualenv](https://virtualenv.pypa.io/en/latest/)
- 🧪 [pytest](https://docs.pytest.org/) + [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) para testes e cobertura
- 🔑 Conta e chave de API da [OpenAI](https://platform.openai.com/)

---

## 🧰 Principais Tecnologias

- 🐍 **Python** & **Django**: Backend e servidor web
- ⚡ **Django Ninja**: Criação de APIs rápidas e documentação automática
- 🤖 **OpenAI GPT-3.5 Turbo**: Modelo de IA usado para a classificação e geração de resposta via API.
- 🧠 **spaCy**: Pré-processamento de texto (lemmatização, stopwords, etc.)
- 📄 **pypdf**: Biblioteca para leitura e extração de texto de arquivos PDF.
- 🎨 **HTML/CSS/JavaScript**: Interface web (incluindo _loading screen_ e _scroll_ dinâmico).
- 🧪 **pytest + pytest-cov**: Testes automatizados e cobertura de código

---

## 🧠 Inteligência Artificial (IA) e Prompt Engineering

O serviço de classificação é centralizado no arquivo `nlp.py` e utiliza uma arquitetura de IA baseada em prompts para garantir precisão e estabilidade na saída de dados.

### Escolha do Modelo

O modelo selecionado para a classificação é o **OpenAI GPT-3.5 Turbo**. Esta escolha é estratégica devido a:

1.  **Baixa Latência e Custo:** É um modelo que oferece alta velocidade de resposta com um custo menor, ideal para processamento em massa de e-mails.
2.  **Habilidade de JSON:** Excelente capacidade de seguir instruções de formato.

### Prompt Engineering e Formato de Resposta

Para garantir a confiabilidade do sistema, a comunicação com a API da OpenAI é rigidamente controlada:

- **Definição de Papel:** O prompt define o papel da IA como um "classificador de emails de uma empresa do setor financeiro".
- **Critérios Claros:** Os critérios de classificação ('Produtivo' vs. 'Improdutivo') são definidos explicitamente no prompt, o que minimiza a subjetividade da IA.
- **Saída Forçada em JSON:** A requisição é configurada para forçar o retorno no formato JSON (`response_format={"type": "json_object"}`), eliminando a necessidade de grandes bibliotecas de validação e assegurando que o _backend_ Django receba os campos `categoria` e `resposta_sugerida` corretamente.

---

## 📝 Processamento de Linguagem Natural (NLP)

O pré-processamento do texto inclui:

- Conversão para minúsculas
- Remoção de espaços em branco extras
- Lematização (redução das palavras à sua forma base)
- Remoção de stopwords e pontuação

Essas etapas são realizadas antes de enviar o texto para a IA, tornando a análise mais eficiente e precisa.

---

## 🔔 Sistema de Logging e Monitoramento

O projeto utiliza um sistema de _logging_ centralizado (`.logger`) para rastrear o fluxo de execução e diagnosticar falhas, sendo crucial para operações com APIs externas.

### Pontos de Registro Principais

- **`views.py`**: Registra o início da requisição POST, validação do tamanho do arquivo e o conteúdo final antes de chamar a IA.
- **`utils.py`**: Monitora o processo de leitura de arquivos (`.txt` e `.pdf`), registrando o tipo de arquivo e possíveis erros durante a extração do texto.
- **`nlp.py`**: Registra o texto bruto de entrada, o texto após o pré-processamento, a resposta JSON exata da OpenAI e trata erros de decodificação JSON ou de conexão com a API.

O sistema usa `logger.info()` para eventos de fluxo normais e `logger.error()` ou `logger.warning()` para capturar falhas e exceções, garantindo que o `exc_info=True` seja usado para erros fatais.

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

## 🐳 Execução com Docker

**Crie um arquivo `.env` na raiz do projeto com sua chave da OpenAI:**

```
OPENAI_API_KEY=sua-chave-aqui
```

🟢 Subir o Docker

```bash
docker-compose up --build
```

🛑 Parar e remover container

```bash
docker-compose down
```

---

## Execução via Makefile

```bash
make setup #Configuração [venv, spacy, nltk, migrate]
```

```bash
source venv/bin/activate #Ativação do ambiente virtual
```

```bash
make run # inicia o servidor
```

---

## 📁 Estrutura do Projeto

```
EMAIL_CLASSIFIER-AUTOU/
├── core/                        # Configurações Globais
│   ├── settings.py              # Definições de ambiente, apps
│   └── urls.py                  # Mapeamento de URL's globais
├── email_classifier/            # Aplicação Principal de Classificação
│   ├── templates/               # Front-End
│   ├── __init__.py
│   ├── api.py                   # Rotas da API Ninja
│   ├── models.py                # Modelos de Banco de Dados (se houver)
│   ├── nlp.py                   # Lógica central: Pré-processamento, Classificação e Geração de Resposta AI
│   └── views.py                 # Views do Django para interface Web
├── tests/                       # Testes unitarios e de integração
├── venv/                        # Ambiente Virtual Python
├── docker-compose.yml           # Configuração para orquestração com Docker
├── Dockerfile                   # Instruções de construção da Imagem Docker
├── manage.py                    # Ferramenta de linha de comando do Django
└── requirements.txt             # Dependências Python do projeto
```

---

## 📊 Cobertura de Código com pytest-cov

A cobertura de código é uma métrica que indica a porcentagem do seu código-fonte que foi executada durante a execução da sua suíte de testes. Ela ajuda a identificar partes do seu código que não estão sendo testadas e que, portanto, podem conter bugs ocultos.

### 📂 Estrutura dos testes

```bash
tests/
└── unit/         # Testes unitários
└── integration/  # Testes de integração da API
```

### Medindo a Cobertura com pytest-cov

O pytest-cov é um plugin para o pytest que integra a medição de cobertura de forma muito simples.

#### Instalação:

```
pip install pytest-cov
```

#### Executando Testes com Cobertura:

Para executar seus testes e gerar um relatório de cobertura no terminal, use a flag `--cov`:

```bash
pytest --cov=email_classifier
```

### Gerando Relatórios Detalhados:

Para uma análise mais aprofundada, você pode gerar relatórios em formatos diferentes:

- Relatório HTML: Cria um HTML para navegar pelos seus arquivos e ver exatamente quais linhas foram ou não cobertas.

```bash
pytest --cov=. --cov-report=html
```

Isso criará um diretório **htmlcov**. Abra o arquivo `index.html` em seu navegador.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
