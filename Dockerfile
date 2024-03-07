FROM ubuntu:22.04

WORKDIR /
RUN apt update
RUN apt install -y python3 python3-pip

RUN python3 -m pip install -U pip
RUN pip install qibocal
COPY . /app

WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install prometheus-client
WORKDIR /app/monitoring

WORKDIR /app
CMD python3 scripts/main.py && qq auto monitoring/monitor.yml -o monitor/report -f && python3 monitoring/monitor-prometheus.py
