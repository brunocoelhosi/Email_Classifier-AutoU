FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Baixa o modelo do spaCy para português
RUN python -m spacy download pt_core_news_sm

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando para rodar as migrações e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]