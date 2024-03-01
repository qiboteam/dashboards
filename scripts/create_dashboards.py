import requests
import json
from pathlib import Path

from utils import grafana_url


def create_time_series(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "time_series.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template["datasource"]["type"] = timeseries_plot["type"]
    panel_template["targets"][0]["datasource"]["type"] = timeseries_plot["type"]
    panel_template["targets"][0]["expr"] = timeseries_plot["metric"]
    panel_template["targets"][0]["legendFormat"] = timeseries_plot["legend"]
    panel_template["title"] = timeseries_plot["title"]
    panel_template["fieldConfig"]["defaults"]["custom"]["axisLabel"] = timeseries_plot["axis_label"]
    if "unit" in timeseries_plot:
        panel_template["fieldConfig"]["defaults"]["unit"] = timeseries_plot["unit"]
    if "color" in timeseries_plot:
        panel_template["fieldConfig"]["overrides"][0]["matcher"]["options"] = timeseries_plot["metric"]
        panel_template["fieldConfig"]["overrides"][0]["properties"][0]["value"] = timeseries_plot["color"]

    panel_template["gridPos"] = timeseries_plot["position"]

    return panel_template

def create_stat(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "stat.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template["datasource"]["type"] = timeseries_plot["type"]
    panel_template["targets"][0]["datasource"]["type"] = timeseries_plot["type"]
    panel_template["targets"][0]["expr"] = timeseries_plot["metric"]
    panel_template["title"] = timeseries_plot["title"]
    panel_template["gridPos"] = timeseries_plot["position"]
    if "unit" in timeseries_plot:
        panel_template["fieldConfig"]["defaults"]["unit"] = timeseries_plot["unit"]
    if "color_steps" in timeseries_plot:
        panel_template["fieldConfig"]["defaults"]["thresholds"]["steps"] = timeseries_plot["color_steps"]
    if "color_mode" in timeseries_plot:
        panel_template["options"]["colorMode"] = timeseries_plot["color_mode"]

    return panel_template


def create_dashboard(dashboard_properties, panels: list = None, http_headers=None):
    if panels is None:
        panels = []
    template_path = Path(__file__).parents[1] / "templates" / "new_dashboard.json"
    dashboard_template = json.loads(template_path.read_text())
    dashboard_template["dashboard"]["title"] = dashboard_properties["title"]
    dashboard_template["dashboard"]["panels"] = panels
    requests.request("POST", grafana_url("dashboards/db"), data=json.dumps(dashboard_template), headers=http_headers)
