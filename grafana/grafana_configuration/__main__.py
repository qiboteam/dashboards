import argparse
import dataclasses
import json
from pathlib import Path

import jinja2
from grafana_configuration import datasources
from grafana_configuration.dashboards import Dashboard

from .api_key import grafana_key
from .users import change_admin_password, create_users
from .utils import DATASOURCE_CONFIGURATION_PATH

HTTP_HEADERS = {
    "Authorization": f"Bearer {grafana_key()}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
GRAFANA_TEMPLATES_PATH = Path(__file__).parent / "templates"


@dataclasses.dataclass
class Metric:
    name: str
    color: str


@dataclasses.dataclass
class MetricPanel:
    title: str
    metrics: list[Metric]
    width: int
    height: int
    unit: str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin", type=str, nargs="?", default=None)
    parser.add_argument("--users", type=str, nargs="?", default=None)
    parser.add_argument(
        "--qpu-config",
        type=Path,
        nargs="?",
        default=Path(__file__).parent / "config" / "qpu_config.json",
    )
    args = parser.parse_args()

    # create defined datasources
    data_sources = json.loads(DATASOURCE_CONFIGURATION_PATH.read_text())
    for data_source in data_sources:
        datasources.create(data_source, http_headers=HTTP_HEADERS)

    coherence_metrics = [
        Metric(name="t1", color="red"),
        Metric(name="t2", color="blue"),
    ]
    fidelity_metrics = [
        Metric(name="assignment_fidelity", color="green"),
    ]
    metric_panels = [
        MetricPanel(
            title="Coherence_times",
            metrics=coherence_metrics,
            width=5,
            height=6,
            unit="ns",
        ),
        MetricPanel(
            title="Fidelities",
            metrics=fidelity_metrics,
            width=5,
            height=6,
            unit="percentunit",
        ),
    ]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(GRAFANA_TEMPLATES_PATH))
    template = env.get_template("coherence_fidelity.json")
    qpu_configuration = json.loads(args.qpu_config.read_text())
    for qpu_config in qpu_configuration["qpus"]:
        json_string = template.render(
            qpu_name=qpu_config["name"],
            qubits=qpu_config["qubits"],
            metric_panels=metric_panels,
        )
        dashboards_configurations = json.loads(json_string)
        for dash_conf in dashboards_configurations:
            dash = Dashboard.from_json_configuration(dash_conf)
            dash.create(http_headers=HTTP_HEADERS)

    if args.users is not None:
        user_configurations = json.loads(args.users)
        for user_configuration in user_configurations:
            create_users(user_configuration)
    if args.admin is not None:
        change_admin_password(args.admin)


if __name__ == "__main__":
    main()
