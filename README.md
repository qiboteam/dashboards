# dashboards

## Installation instruction

Docker containers can be set up with
``` bash
docker compose up
```

**_NOTE:_**  Docker should be used as a non-root user:
https://docs.docker.com/engine/install/linux-postinstall/

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

## Plugins

The Grafana Docker allows installation of plugins on startup, we've included some plugins needed for the automatic configuration of dashboards.
Please add the following line to the `.env` file to install the plugins, create the blank .env file if it doesn't exist.
``` bash
GF_INSTALL_PLUGINS=yesoreyeram-infinity-datasource,nline-plotlyjs-panel,serrrios-statusoverview-panel
```
If you want to add or remove plugins, you can do so by changing the list in the `.env` file,
Using the plugin name as it appears in the Grafana plugin repository url, i.e. `nline-plotlyjs-panel` in https://grafana.com/grafana/plugins/nline-plotlyjs-panel/.

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
```

A reference file can be found at `grafana_configuration/config/qpu_config.json`.

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

The list of qpu (and qubits) on which to run the monitoring needs to be defined in the `.env` file:

``` bash
MONITORING_CONFIGURATION='[{"partition":"slurm_partition_name","platform":"qpu_name","targets":["0", "1"]}]'
```

The path to the `qibolab` platforms used by the monitoring script need to be specified in the `.env` file:

``` bash
QIBOLAB_PLATFORMS_PATH=/path/to/qibolab/platforms/directory
```

Every time the monitoring container starts, a single monitoring instance is run. In order to monitor again, the
container needs to be restarted with the following command:

``` bash
docker restart remote_monitoring
```

## Backup of SQL data

When stopping containers with `docker compose down`, all data not stored on persistent volumes
(i.e.: bind mounts of docker volumes) are lost.

If you want to save data stored in `postgres` (qpu metrics), it is possible to dump them to the host with the command

``` bash
sh db_backup.sh
```

On the next startup with `docker compose up`, it is possible to restore the database with the command

``` bash
sh db_restore.sh
```

> [!NOTE]
> Currently the database needs to be restored as soon as the container starts (before remote_monitoring commits data).
