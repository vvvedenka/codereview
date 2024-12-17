FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV BOT_TOKEN=7947881343:AAFwarC1O2Mr8nBsGSp50r1VbYyNDJWc9BU
ENV POSTGRES_USER=vvvedenka
ENV POSTGRES_PASSWORD=1230
ENV POSTGRES_DB=vvvedenka
COPY . /app
CMD ["python3", "bot.py"]
