FROM python:3.10-slim-bullseye

COPY . /app

WORKDIR /app/src

COPY requirements.txt requirements.txt

RUN apt-get update -y && \
    apt-get install -y build-essential python3-dev python3-setuptools curl && \
    pip install --upgrade --no-cache-dir pip && \
    apt-get install libpq-dev -y

RUN pip install -r requirements.txt 

ENV PYTHONPATH=/app/src