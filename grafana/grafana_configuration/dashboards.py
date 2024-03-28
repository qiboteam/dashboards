import json

import grafanalib.core as glc
import requests
from grafana_configuration.dashboard_elements.row import Row
from grafana_configuration.dashboard_elements.timeseries import Stat, TimeSeries
from grafana_configuration.dashboard_elements.utils import GridPos
from grafanalib._gen import DashboardEncoder

from .utils import GRAFANA_URL


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
            "Target": glc.Target,
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
        return dashboard


def create(dashboard_configuration: dict, http_headers: dict[str, str]):
    """Create a new dashboard.

    Args:
        dashboard_configuration (dict): parameters of the new dashboard
            that are set and then exported to grafana.
        http_headers (dict[str, str]): http headers for the request containing the API key.
    """
    dashboard = Dashboard.from_json_configuration(dashboard_configuration)
    requests.post(
        f"{GRAFANA_URL}/dashboards/db",
        data=dashboard.to_json(),
        headers=http_headers,
    )
