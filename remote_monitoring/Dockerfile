FROM ubuntu:22.04

RUN apt update && apt -y upgrade
RUN apt install -y python3 python3-pip
RUN apt install -y git
RUN apt -y install libpq-dev

COPY . /app
WORKDIR /app
RUN python3 -m pip install .

CMD python3 -m remote_monitoring --host $REMOTE_HOST --username $REMOTE_USERNAME --private_key_password $SSH_KEY_PASSWORD --slurm_configuration $MONITORING_CONFIGURATION
