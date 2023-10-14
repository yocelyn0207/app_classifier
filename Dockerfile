#!/bin/bash
FROM python:3.8-slim

WORKDIR /use_class_classifier

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc curl unzip sudo

COPY ./requirements.txt /use_class_classifier/requirements.txt
RUN pip3 install --no-cache-dir -r /use_class_classifier/requirements.txt

COPY . /use_class_classifier

#CMD gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 api:app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]