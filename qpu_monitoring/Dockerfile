FROM ubuntu:22.04

RUN apt update && apt -y upgrade
RUN apt install -y python3 python3-pip
RUN apt install -y slurm-client

RUN python3 -m pip install -U pip
RUN apt install -y git
RUN git clone https://github.com/qiboteam/qibocal
RUN cd qibocal; pip install .
# RUN pip install qibocal
COPY runcards /app/runcards
COPY scripts /app/scripts
# COPY /etc/slurm /etc/slurm

RUN pip install prometheus-client

WORKDIR /app
CMD ./scripts/monitor.sh $SLURM_PARTITION
