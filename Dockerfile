FROM python:3.10.12-slim


WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y iputils-ping curl postgresql-client && apt-get clean
RUN pip install --upgrade pip && pip install -r requirements.txt && rm -rf requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Copiando o restante do código
COPY . /app/

# Exponha a porta 8000
EXPOSE 8000

# Execute as migrações e inicia o servidor Django
CMD ["sh", "/start.sh"]
