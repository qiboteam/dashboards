#!/bin/bash

gunzip < .postgres_dump.gz | docker exec -i postgres psql -U dash_admin -d qpu_metrics
