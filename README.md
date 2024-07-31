# dashboards

## Installation instruction

Docker containers can be set up with
``` bash
docker compose up
```

### qpu_monitoring

`qpu_monitoring` requires `psycopg2` which in turn requires `pg_config`.
`pg_config` is in `postgresql-devel`, which can be installed with:
``` bash
apt install libpq-dev
```

## Containers

Currently the following containers are created:
 - `grafana` with a Grafana server, exposing port `3000`.
 - `grafana_setup` containing scripts for automatic configuration of grafana.
 Starts running only after `grafana` is fully running. It stops immediately after.
 - `prometheus` containing a Prometheus server, exposing port `9090`.
 - `pushgateway` containing https://github.com/prometheus/pushgateway server, exposing port `9091`.
 It can be used for sending metrics, which will then be scraped by Prometheus.
 - `monitoring` containing a Ubuntu image with `qibocal` to be restarted at regular intervals for acquiring QPU metrics.

## Grafana users

By default grafana only creates an account with admin privileges with username `admin` and password `admin`.
Its password can be changed and other users may be created by setting environment variables in a `.env` file placed at the root of this repository.
A `.env` file will look like this:
``` bash
ADMIN_PASSWORD=new_admin_password
GRAFANA_USERS='[{"login":"first_user","password":"first_password"},{"login":"second_user","password":"second_password","role":"Editor"}]'
```

## QPUs

An optional list of QPUs can be provided to the initialization script in a json file.
``` json
{
    "qpus": [
        {
            "name": "1st qpu name",
            "qubits": 5
        },
        {
            "name": "2nd qpu name",
            "qubits": 3
        },
    ]
}
```
For each QPU listed, the script generates a dashboard showing coherence times and assignment fidelity.

A reference file (used by default) can be found at `grafana_configuration/config/qpu_config.json`.
