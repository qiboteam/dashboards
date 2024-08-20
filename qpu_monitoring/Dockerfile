FROM alpine:3.19

RUN apk update
RUN apk add python3 py3-pip

COPY . /app
WORKDIR /app
RUN pip install . --break-system-packages

CMD python scripts/monitoring_connection.py
