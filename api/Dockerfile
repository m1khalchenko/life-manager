FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /usr/src/api

COPY ./requirements.txt /usr/src/api/
RUN pip install -r /usr/src/api/requirements.txt
RUN pip install uvicorn
WORKDIR /usr/src/api
COPY . /usr/src/api
