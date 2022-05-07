FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

COPY . /app

CMD ["python", "/app/src/app.py", "viagens.csv"]