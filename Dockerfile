FROM python:3.11-alpine

COPY requirements.txt /temp/requirements.txt
COPY /core /core

RUN pip install -r /temp/requirements.txt && adduser --disabled-password service_user
WORKDIR /core
EXPOSE 8000

USER service_user
