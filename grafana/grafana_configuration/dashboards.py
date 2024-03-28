import json

import grafanalib.core as glc
import requests
from grafana_configuration.dashboard_elements.row import Row
from grafana_configuration.dashboard_elements.utils import GridPos
from grafanalib._gen import DashboardEncoder

from .utils import GRAFANA_URL


class Dashboard(glc.Dashboard):
    """Wrapper class of `grafanalib.core.Dashboard`."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        TODO: add also panels in the row."""
        self.panels.append(row)


def create(dashboard_configuration: dict, http_headers: dict[str, str]):
    """Create a new dashboard.

    Args:
        dashboard_configuration (dict): parameters of the new dashboard
            that are set and then exported to grafana.
        http_headers (dict[str, str]): http headers for the request containing the API key.
    """
    # TODO: move it to a dedicated class method
    dashboard = Dashboard(title=dashboard_configuration["title"])
    if "rows" in dashboard_configuration:
        for row in dashboard_configuration["rows"]:
            dashboard_row = Row(row["title"], GridPos(**row["grid_pos"]))
            dashboard.add_row(dashboard_row)
    requests.post(
        f"{GRAFANA_URL}/dashboards/db",
        data=dashboard.to_json(),
        headers=http_headers,
    )
