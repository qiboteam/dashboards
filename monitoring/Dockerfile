FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3 python3-pip

RUN python3 -m pip install -U pip
RUN pip install qibocal
COPY runcards /runcards

RUN pip install prometheus-client

WORKDIR /runcards
CMD sleep inf
