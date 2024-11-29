import argparse
import dataclasses
import requests
import json
from pathlib import Path

import jinja2
from grafana_configuration import dashboards, datasources
from grafanalib.core import (
    Dashboard, TimeSeries, GaugePanel, RowPanel,
    Target, GridPos
)
from grafanalib._gen import DashboardEncoder

from .api_key import grafana_key
from .users import change_admin_password, create_users
from .utils import DATASOURCE_CONFIGURATION_PATH
from .utils import ADMIN_PASSWORD, ADMIN_USERNAME, GRAFANA_URL

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


'''
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
    # Work around for argparse bug
    if args.qpu_config is None:
        qpu_configuration = json.loads(
            (Path(__file__).parent / "config" / "qpu_config.json").read_text()
        )
    else:
        qpu_configuration = json.loads(args.qpu_config.read_text())
    # Create dashboards for each qpu
    for qpu_config in qpu_configuration["qpus"]:
        if "edges" not in qpu_config or len(qpu_config["edges"]) == 0:
            json_string = template.render(
                qpu_name=qpu_config["name"],
                qubits=qpu_config["qubits"],
                metric_panels=metric_panels,
            )
        else:
            # Preprocessing edges to create the string used in grafana
            edge_string = "id,source,target\\r\\n"
            for edges in qpu_config["edges"]:
                edge_string += f"0,{edges[0]},{edges[1]}\\r\\n"
            json_string = template.render(
                qpu_name=qpu_config["name"],
                qubits=qpu_config["qubits"],
                edge_string="\"" + edge_string + "\"",
                metric_panels=metric_panels,
            )
        dashboards_configurations = json.loads(json_string)
        for dash in dashboards_configurations:
            dashboards.create(dash, http_headers=HTTP_HEADERS)

    if args.users is not None:
        user_configurations = json.loads(args.users)
        for user_configuration in user_configurations:
            create_users(user_configuration)
    if args.admin is not None:
        change_admin_password(args.admin)

    dashboard_json = get_dashboard_json(test_dashboard, overwrite=True)
    upload_to_grafana(dashboard_json, GRAFANA_URL, grafana_key)
    print(parse_config(args.qpu_config))
'''

'''
test_dashboard = Dashboard(
    title="Python generated example dashboard",
    description="Example dashboard using the Random Walk and default Prometheus datasource",
    tags=[
        'example'
    ],
    timezone="browser",
    panels=[
        TimeSeries(
            title="Random Walk",
            dataSource='default',
            targets=[
                Target(
                    datasource='grafana',
                    expr='example',
                ),
            ],
            gridPos=GridPos(h=8, w=16, x=0, y=0),
        ),
        RowPanel(title="New row", gridPos=GridPos(h=1, w=24, x=0, y=8)),
        GaugePanel(
            title="Random Walk",
            dataSource='default',
            targets=[
                Target(
                    datasource='grafana',
                    expr='example',
                ),
            ],
            gridPos=GridPos(h=4, w=4, x=0, y=10),
        ),
        RowPanel(title="New row 2", gridPos=GridPos(h=1, w=24, x=0, y=15)),
        GaugePanel(
            title="Random Walk 2",
            dataSource='default',
            targets=[
                Target(
                    datasource='grafana',
                    expr='example',
                ),
            ],
            gridPos=GridPos(h=4, w=4, x=0, y=16),
        ),
    ],
).auto_panel_ids()
'''


def parse_config(qpu_config=None):
    if qpu_config is None:
        qpu_configuration = json.loads(
            (Path(__file__).parent / "config" / "qpu_config.json").read_text()
        )
    else:
        qpu_configuration = json.loads(qpu_config.read_text())
    # print(qpu_configuration)
    return qpu_configuration


def generate_dashboard(qpu):

    # Options
    gridposY = 0  # Running counter for y position of panels, might make more sense to make functions reutrn a tupple so Y can be updated
    defPanelH = 8
    defPanelW = 8


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

    panels = [] # List of panels to be added to the dashboard
    qpu_node_data = "id,source,target"
    for i, (a, b) in enumerate(qpu["edges"]):
        qpu_node_data += f"\n{i},{a},{b}"
    print(qpu_node_data)
    panels.append(dashboards.generate_node_graph_panel(qpu["name"], qpu_node_data, gridPos=GridPos(h=defPanelH, w=defPanelW, x=0, y=gridposY)), )
    gridposY += defPanelH + 1

    for metric in metric_panels:
        panels.append(RowPanel(title=metric.title, gridPos=GridPos(h=1, w=24, x=0, y=gridposY)), )
        gridposY += 1
        for i in range(qpu['qubits']):
            gridPos = GridPos(h=defPanelH, w=defPanelW, x=i * defPanelW, y=gridposY)
            panels.append(dashboards.generate_time_series_panel(qpu, i, gridPos, metric.title))
        gridposY += defPanelH + 1

    qpu_dashboard = Dashboard(
        title=qpu['name'],
        description=f'Example dashboard using the Random Walk and default Prometheus datasource for {qpu["name"]}',
        tags=[
            'example'
        ],
        timezone="browser",
        panels=panels,
    ).auto_panel_ids()

    return qpu_dashboard


def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
    '''
    get_dashboard_json generates JSON from grafanalib Dashboard object

    :param dashboard - Dashboard() created via grafanalib
    '''

    # grafanalib generates json which need to pack to "dashboard" root element
    return json.dumps(
        {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite
        }, sort_keys=True, indent=2, cls=DashboardEncoder)


def upload_to_grafana(json, server, api_key, auth, verify=True):
    '''
    upload_to_grafana tries to upload dashboard to grafana and prints response

    :param json - dashboard json generated by grafanalib
    :param server - grafana server name
    :param api_key - grafana api key with read and write privileges
    :param auth - authentication tuple (username, password)
    '''

    headers = {'Authorization': f"Bearer {api_key}", 'Content-Type': 'application/json'}
    return requests.post(f"{server}/dashboards/db", data=json, headers=headers, verify=verify, auth=auth)


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

    qpu_config = parse_config(args.qpu_config)
    for qpu in qpu_config['qpus']:
        qpu_dashboard = generate_dashboard(qpu)
        dashboard_json = get_dashboard_json(qpu_dashboard, overwrite=True)
        upload_to_grafana(dashboard_json, GRAFANA_URL, grafana_key, (ADMIN_USERNAME, ADMIN_PASSWORD))


if __name__ == "__main__":
    main()
