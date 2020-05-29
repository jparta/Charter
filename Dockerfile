FROM python:3.5-alpine3.9

WORKDIR /dockerapp

# Building tools for python libraries
RUN apk add gcc
RUN apk add musl-dev
RUN apk add postgresql-dev
# To download a-plus-client in requirements.txt
RUN apk add --no-cache git
RUN pip install --upgrade pip

# Exclusions in .dockerignore
COPY . .

RUN pip install -r ./requirements.txt


# ---
#FROM apluslms/service-base:python3-1.5

#COPY rootfs /
#ENTRYPOINT [ "/init", "run-django.sh" ]
