FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY scraper.py /app/scraper.py
CMD ["python3", "bot.py"]
