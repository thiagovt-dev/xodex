# Dockerfile minimal para rodar o agente via 'agente-ia'
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências de runtime do sistema (opcional: git para :git comandos)
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Copia projeto e instala como pacote
COPY . /app
RUN pip install --no-cache-dir .

# Copie seu .env se quiser embutir config no container
# COPY .env /app/.env

# Comando padrão
CMD ["xodex"]
