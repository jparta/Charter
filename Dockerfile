FROM python:3.5-alpine3.9

WORKDIR /dockerapp

RUN apk add gcc
RUN apk add musl-dev
RUN apk add postgresql-dev
RUN apk add --no-cache git
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY app ./app/
COPY instance ./instance/
COPY images ./images/
COPY entrypoint_api.py ./
COPY entrypoint_celery.py ./
COPY .flaskenv ./
