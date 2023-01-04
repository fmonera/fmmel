# syntax=docker/dockerfile:1
# 

FROM python:3.10-bullseye

RUN echo "Building fmmel."
RUN echo "Based on python:3.10-bullseye"

WORKDIR /

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./app /app
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000

COPY ./scripts/start.sh /start.sh

ENTRYPOINT ["/start.sh"]

