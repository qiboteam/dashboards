import json
import attr
from attr.validators import instance_of

import grafanalib.core as glc
import requests
from grafana_configuration.dashboard_elements.panels import Stat, TimeSeries
from grafana_configuration.dashboard_elements.row import Row
from grafana_configuration.dashboard_elements.targets import Target
from grafana_configuration.dashboard_elements.utils import GridPos
from grafanalib._gen import DashboardEncoder
from grafanalib.core import TimeSeries, SqlTarget, Panel

from .utils import GRAFANA_URL

'''
class Dashboard(glc.Dashboard):
    """Wrapper class of `grafanalib.core.Dashboard`."""

    def __init__(self, *args, timezone: str = "browser", **kwargs):
        """Create an empty dashboard.

        Args:
            timezone (str): timezone used by plots.
                supported values: "browser", "utc" (default for grafanalib),
                "" (default for grafana), region/city or region/state/city
        """
        super().__init__(*args, timezone=timezone, **kwargs)

    @property
    def to_json(self) -> str:
        """Convert dashboard into a json string ready to be imported in grafana."""
        return json.dumps(
            {
                "dashboard": self.to_json_data(),
                "overwrite": True,
            },
            sort_keys=True,
            indent=2,
            cls=DashboardEncoder,
        )

    def add_row(self, row: Row):
        """Add row to the dashboards.

        Args:
            row (Row): row element of the dashboard. It can contain dashboard panels.
        """
        self.panels.append(row)
        for panel in row.panels:
            self.panels.append(panel)

    @classmethod
    def from_json_configuration(cls, dashboard_configuration: dict):
        """Create a dashboard object from a configuration dictionary.

        Args:
            dashboard_configuration (dict): parameters of the new dashboard
                that are set and then exported to grafana.
        """
        class_lookup = {
            "TimeSeries": TimeSeries,
            "Stat": Stat,
            "Target": Target,
        }
        dashboard = cls(title=dashboard_configuration["title"])
        if "rows" in dashboard_configuration:
            for row in dashboard_configuration["rows"]:
                dashboard_row = Row(row["title"], GridPos(**row["grid_pos"]))
                if "panels" in row:
                    for panel in row["panels"]:
                        panel_class = class_lookup[panel["type"]]
                        grid_pos = GridPos(**panel["value"]["grid_pos"])
                        panel["value"]["grid_pos"] = grid_pos
                        dashboard_targets = []
                        for target in panel["value"]["targets"]:
                            target_class = class_lookup[target["type"]]
                            dashboard_targets.append(target_class(**target["value"]))
                        panel["value"]["targets"] = dashboard_targets
                        dashboard_panel = panel_class(**panel["value"])
                        dashboard_row.add(dashboard_panel)
                dashboard.add_row(dashboard_row)
        print(dashboard)
        return dashboard


def create(dashboard_configuration: dict, http_headers: dict[str, str]):
    """Create a new dashboard.

    Args:
        dashboard_configuration (dict): parameters of the new dashboard
            that are set and then exported to grafana.
        http_headers (dict[str, str]): http headers for the request containing the API key.
    """
    dashboard = Dashboard.from_json_configuration(dashboard_configuration)
    print(dashboard.to_json)
    requests.post(
        f"{GRAFANA_URL}/dashboards/db",
        data=dashboard.to_json,
        headers=http_headers,
    )
'''

def generate_time_series_panel(qpu, i, gridPos, metric):
    time_series = TimeSeries(
            title=metric,
            dataSource='postgres',
            targets=[
                SqlTarget(
                    rawSql=f'SELECT {metric}, acquisition_time FROM qubit WHERE qpu_name="{qpu["name"]}" AND qubit_id={i}',
                ),
            ],
            gridPos=gridPos,
    )
    return time_series


def generate_node_graph_panel(qpu, qpu_node_data, gridPos):
    node_graph = NodeGraph(
            title=qpu,
            AData=qpu_node_data,
            gridPos=gridPos,
    )
    return node_graph

@attr.s
class NodeGraph(Panel):

    """Generates Node Graph panel json structure using infinity

    Grafana doc on time series: https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/node-graph/
    Infinity doc: https://grafana.com/docs/plugins/yesoreyeram-infinity-datasource/latest/

    :param optionEdges
    :param optionNodes
    :param AColumns
    :param AData
    :param AFilters
    :param AFormat
    :param ASource
    :param AType
    """

    optionEdges = attr.ib(default=attr.Factory(dict), validator=instance_of(dict))
    optionNodes = attr.ib(default=attr.Factory(dict), validator=instance_of(dict))
    AColumns = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    AData = attr.ib(default='', validator=instance_of(str))
    AFilters = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    AFormat = attr.ib(default='table', validator=instance_of(str))
    ASource = attr.ib(default='inline', validator=instance_of(str))
    AType = attr.ib(default='csv', validator=instance_of(str))

    def to_json_data(self):
        return self.panel_json({
              "datasource": {
                "type": "datasource",
                "uid": "-- Mixed --"
              },
              "options": {
                "edges": self.optionEdges,
                "nodes": self.optionNodes
              },
              "targets": [
                {
                  "columns": self.AColumns,
                  "data": self.AData,
                  "datasource": {
                    "type": "yesoreyeram-infinity-datasource",
                    "uid": "be5anox316c5ca"
                  },
                  "filters": self.AFilters,
                  "format": self.AFormat,
                  "global_query_id": "",
                  "refId": "A",
                  "root_selector": "",
                  "source": self.ASource,
                  "type": self.AType,
                  "url": "",
                  "url_options": {
                    "data": "",
                    "method": "GET"
                  }
                },
                {
                  "datasource": {
                    "type": "datasource",
                    "uid": "grafana"
                  },
                  "hide": False,
                  "refId": "B"
                }
              ],
              "title": "Panel Title",
              "type": "nodeGraph"
            },
        )