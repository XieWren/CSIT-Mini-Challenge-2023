# Docker Images: https://hub.docker.com/repository/docker/xiewren/csit-mini-challenge-2023/general
FROM tiangolo/uvicorn-gunicorn:python3.11-slim
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf requirements.txt
COPY src/ ./

EXPOSE 8080
CMD [ "python", "main.py" ]