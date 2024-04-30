FROM alpine:3.19

RUN apk update
RUN apk add python3 py3-pip

COPY monitoring /app
WORKDIR /app
RUN pip install pyyaml prometheus-client --break-system-packages
RUN pip install qibolab --break-system-packages

CMD python3 monitor.py --name $CRYO_NAME --ip $CRYO_IP --port $CRYO_PORT
