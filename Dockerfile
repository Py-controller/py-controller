FROM python:3.11.1-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app/py_controller

COPY . /app/py_controller/

RUN pip install -U pip
RUN pip install -r requirements.txt