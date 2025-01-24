#!/bin/bash

docker exec -t postgres pg_dumpall -c -U dash_admin | gzip > .postgres_dump.gz
