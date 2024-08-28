FROM alpine:3.19

RUN apk update
RUN apk add python3 py3-pip
RUN apk add openssh

COPY . /app
WORKDIR /app
RUN pip install . --break-system-packages
