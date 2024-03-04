FROM ubuntu:22.04

WORKDIR /
RUN apt update
RUN apt install -y python3 python3-pip

RUN python3 -m pip install -U pip
COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD python3 scripts/main.py
