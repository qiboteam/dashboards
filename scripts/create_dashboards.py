import copy
import json
from pathlib import Path

import requests
from utils import grafana_url


def add_traces(template, parameters):
    template["datasource"]["type"] = parameters["metrics"][0].db_type
    template["title"] = parameters["title"]

    targets_template = template["targets"][0]
    template["targets"] = []
    color_template = template["fieldConfig"]["overrides"][0]
    template["fieldConfig"]["overrides"] = []

    for i, metric in enumerate(parameters["metrics"]):
        metric_target_template = copy.deepcopy(targets_template)
        metric_target_template["datasource"]["type"] = metric.db_type
        metric_target_template["expr"] = metric.metric

        if len(metric.metric_filters) > 0:
            metric_target_template["expr"] += "{"
            for filter in metric.metric_filters:
                filter[-1] = rf'"{filter[-1]}"'
                metric_target_template["expr"] += "".join(filter)
                metric_target_template["expr"] += ", "
            metric_target_template["expr"] = metric_target_template["expr"][:-2]
            metric_target_template["expr"] += "}"
        metric_target_template["legendFormat"] = metric.legend_name
        metric_target_template["refId"] = chr(ord("a") + i)
        template["targets"].append(metric_target_template)

        metric_color_template = copy.deepcopy(color_template)
        metric_color_template["matcher"]["options"] = metric.legend_name
        if metric.color["mode"] == "absolute":
            metric_color_template["properties"][0]["id"] = "thresholds"
        metric_color_template["properties"][0]["value"] = metric.color
        template["fieldConfig"]["overrides"].append(metric_color_template)

    if "unit" in parameters:
        template["fieldConfig"]["defaults"]["unit"] = parameters["unit"]
    return template


def create_time_series(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "time_series.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template = add_traces(panel_template, timeseries_plot)
    panel_template["fieldConfig"]["defaults"]["custom"]["axisLabel"] = timeseries_plot[
        "axis_label"
    ]

    panel_template["gridPos"] = timeseries_plot["position"]

    return panel_template


def create_stat(timeseries_plot):
    panel_template_path = Path(__file__).parents[1] / "templates" / "stat.json"

    panel_template = json.loads(panel_template_path.read_text())
    panel_template = add_traces(panel_template, timeseries_plot)
    panel_template["gridPos"] = timeseries_plot["position"]
    if "color_steps" in timeseries_plot:
        panel_template["fieldConfig"]["defaults"]["thresholds"]["steps"] = (
            timeseries_plot["color_steps"]
        )
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
    requests.request(
        "POST",
        grafana_url("dashboards/db"),
        data=json.dumps(dashboard_template),
        headers=http_headers,
    )
