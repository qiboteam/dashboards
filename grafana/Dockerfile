FROM alpine:3.19

RUN apk update
RUN apk add python3 py3-pip

COPY . /app
WORKDIR /app
RUN pip install . --break-system-packages

CMD python3 -m grafana_configuration --users $GRAFANA_USERS --admin $ADMIN_PASSWORD --qpu-config $QPU_CONFIG_JSON_PATH_CONTAINER
