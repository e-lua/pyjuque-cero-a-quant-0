FROM python:3.8.16-bullseye

ADD . usr/src/app01

WORKDIR /usr/src/app01

RUN pip install -r requeriments.txt

ENTRYPOINT python main.py
