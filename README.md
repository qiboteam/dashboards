# dashboards

## Installation instruction

Docker containers can be set up with
``` bash
docker compose up
```

**_NOTE:_**  Docker should be used as a non-root user:
https://docs.docker.com/engine/install/linux-postinstall/

An update in the docker container requires 
``` bash
docker compose up --build
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


## Addition of Experiments

### To add experiments to monitor in the dashboards the following files are modified:

1. The `qpu_monitoring/scripts/monitoring.py` file is modified. The experiment_output and experiment_name represent the name of the output and the actual name of the operation, respectively. Parameter1, parameter2, and parameter3 are the names of the parameters for the experiment with X, Y, Z being the respective assigned values.

``` python
def main(targets: list, platform_name: str, output_folder: str):
    with Executor.open(
        "myexec",
        path=output_folder,
        platform=platform_name,
        targets=targets,
        update=False,
        force=True,
    ) as e:
        experiment_output = e.experiment_name(
            parameter1 = X,
            parameter2=Y,
            parameter3=Z,
        )
        check_chi2(file_output, platform=e.platform, targets=targets)
 ```

2. In the `remote_monitoring` container the `remote_monitoring/database_schema.py` and `remote_monitoring/metrics_export.py` files are altered.

In the `experiments.py` file, the output metric for each supported experiment is specified. New metrics can be added, as explained in the following example:

``` python
METRICS = {
    "t1": "t1",
    "ramsey": "t2",
    "readout_characterization": "assignment_fidelity",
    "experiment_name": "output_parameter"
}
```

In the database_schema.py file the mapping type of the output value is established in the class Qubit. The Output_Parameter is the output parameter that will appear on the dashboard with Type being the type of that parameter (str, float etc).

``` python
Output_Parameter: Mapped[Type]
```

3. In the grafana container, `/grafana_configuration/__main__.py`uses pre-build templates based on python classes defined in `/grafana_configuration/templates/`.
Panels are gouped into group blocks, that can be placed next to other blocks.
Currently, the coherence-fidelity dashboard is used.

Here us an example on how to add a new row (below the row with assignment fidelities) in the coherence-fidelity dashboard with a new metric:

``` python
class CoherenceFidelityDashboard(Dashboard):
    def __init__(
        self,
        *args,
        title: str = "",
        qubits: Optional[list] = None,
        timezone: str = "browser",
        **kwargs,
    ):
    ...
        new_row = Row(title="Fidelities").below(fidelity_row)
        previous = new_row
        for qubit in self.qubits:
            fidelity_metrics = [
                Metric(
                    name="Output_Parameter",
                    color="Color",
                    qpu_name=self.title,
                    qubit_id=qubit,
                ),
            ]
            group = CoherenceFidelityGroup(
                metrics=fidelity_metrics,
                title="Panel_Title",
                unit="Output_Unit",
            ).right_of(previous)
            previous = group
            new_row.add_group(group)
        self.add_row(new_row)
```

Furthermore, other metrics can be added to existing groups, e.g.:

``` python
class CoherenceFidelityDashboard(Dashboard):
    def __init__(
        self,
        *args,
        title: str = "",
        qubits: Optional[list] = None,
        timezone: str = "browser",
        **kwargs,
    ):
    ...
        fidelity_row = Row(title="Fidelities").below(coherence_row)
        previous = fidelity_row
        for qubit in self.qubits:
            fidelity_metrics = [
                Metric(
                    name="assignment_fidelity",
                    color="green",
                    qpu_name=self.title,
                    qubit_id=qubit,
                ),
                Metric(
                    name="Output_Parameter",
                    color="Color",
                    qpu_name=self.title,
                    qubit_id=qubit,
                ),
            ]
            group = CoherenceFidelityGroup(
                metrics=fidelity_metrics,
                title=f"Qubit {qubit}",
                unit="percentunit",
            ).right_of(previous)
            previous = group
            fidelity_row.add_group(group)
        self.add_row(fidelity_row)
```
