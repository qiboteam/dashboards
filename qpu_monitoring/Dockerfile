FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3 python3-pip

RUN python3 -m pip install -U pip
RUN pip install qibocal
COPY runcards /app/runcards
COPY scripts /app/scripts

RUN pip install prometheus-client

WORKDIR /app
CMD ./scripts/monitor.sh $SLURM_PARTITION
