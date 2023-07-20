FROM python:3.11
LABEL authors="kosiv"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tele_bot

COPY requeriments.txt .
RUN pip install -r requeriments.txt

COPY . .

ENV PYTHONPATH /src

RUN pip install --upgrade pip

RUN chmod -R 777 ./
