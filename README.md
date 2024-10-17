# dashboards

## Installation instruction

Docker containers can be set up with
``` bash
docker compose up
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
 - `postgres` running PostgreSQL 15.6 and containing the database for all QPU metrics acquired.
 - `remote_monitoring` containing an Alpine image that connects to the QPU cluster via SSH.
    After the experiment finishes, the container acquires all measurements and uploads them to `postgres`.

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
            "qubits": [0, 1, 2, 3, 5]
        },
        {
            "name": "2nd qpu name",
            "qubits": ["0", "1", "2", "3"]
        },
    ]
}
```
For each QPU listed, the script generates a dashboard showing coherence times and assignment fidelity.
The path of the json file can be saved in the `.env` file as:
``` bash
QPU_CONFIG_JSON_PATH=/path/to/local/json/file.json
QPU_CONFIG_JSON_PATH_CONTAINER=/conf/qpu_config.json
```

A reference file (used by default) can be found at `grafana_configuration/config/qpu_config.json`.

### Monitoring on slurm clusters

Monitoring of QPUs on slurm clusters can be performed by the `remote_monitoring` container.
In order to connect to the cluster over ssh, the own user's ssh key is required.

Additionally, after the ssh connection in enstablished, the conainer assumes that a Python virtual environment
named `.qpu_monitoring_env` is located in the home directory. Assuming that the `dashboards` repository
has been cloned to the home directory, the environment can be created with the following commands:

``` bash
cd ~
python -m venv .qpu_monitoring_env
cd dashboards/qpu_monitoring
pip install .
```
