FROM python:3.5-alpine3.9

WORKDIR /dockerapp

# Exclusions in .dockerignore
COPY . .

RUN apk add gcc
RUN apk add musl-dev
RUN apk add postgresql-dev
RUN apk add --no-cache git

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
