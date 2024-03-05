import requests
import json
from pathlib import Path
import copy

from utils import grafana_url


def add_traces(template, parameters):
    template["datasource"]["type"] = parameters["type"][0]
    template["title"] = parameters["title"]
    targets_template = template["targets"][0]
    template["targets"] = []
    metrics = parameters["metric"]
    for i, _ in enumerate(metrics):
        metric_target_template = copy.deepcopy(targets_template)
        metric_target_template["datasource"]["type"] = parameters["type"][i]
        metric_target_template["expr"] = parameters["metric"][i]
        if "legend" in parameters:
            metric_target_template["legendFormat"] = parameters["legend"][i]
        metric_target_template["refId"] = chr(ord('a') + i)
        template["targets"].append(metric_target_template)
    if "unit" in parameters:
        template["fieldConfig"]["defaults"]["unit"] = parameters["unit"]
    if "color" in parameters:
        color_template = template["fieldConfig"]["overrides"][0]
        template["fieldConfig"]["overrides"] = []
        for i, _ in enumerate(metrics):
            metric_color_template = copy.deepcopy(color_template)
            metric_color_template["matcher"]["options"] = parameters["metric"][i]
            metric_color_template["properties"][0]["value"] = parameters["color"][i]
            template["fieldConfig"]["overrides"].append(metric_color_template)
    return template


def create_time_series(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "time_series.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template = add_traces(panel_template, timeseries_plot)
    panel_template["fieldConfig"]["defaults"]["custom"]["axisLabel"] = timeseries_plot["axis_label"]

    panel_template["gridPos"] = timeseries_plot["position"]

    return panel_template

def create_stat(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "stat.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template = add_traces(panel_template, timeseries_plot)
    panel_template["gridPos"] = timeseries_plot["position"]
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
