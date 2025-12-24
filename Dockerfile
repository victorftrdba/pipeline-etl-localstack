# Usando uma imagem leve de Python
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas os requisitos primeiro (cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script
COPY app.py .

# Comando para rodar a aplicação
CMD ["python", "app.py"]