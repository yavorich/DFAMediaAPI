FROM python:3.10.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./rest /app/rest
ADD ./docker /app/docker

RUN chmod +x /app/docker/rest/server-entrypoint.sh
RUN chmod +x /app/docker/rest/worker-entrypoint.sh