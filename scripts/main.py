try:
    from api_key import GRAFANA_KEY
except:
    exit()
from create_dashboards import create_dashboard, create_stat, create_time_series
from create_datasources import create_data_source

HTTP_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

from dataclasses import dataclass
from typing import Dict


@dataclass
class Metric:
    metric: str
    metric_filters: list[list[str]]
    legend_name: str
    db_type: str
    color: Dict[str, str]


if __name__ == "__main__":
    # create data sources
    data_sources = [{"name": "prometheus"}]
    for data_source in data_sources:
        create_data_source(data_source, http_headers=HTTP_HEADERS)

    t1 = Metric(
        "t1",
        [["instance", "=", "pushgateway:9091"]],
        "t1",
        "prometheus",
        {"fixedColor": "red", "mode": "fixed"},
    )
    t2 = Metric(
        "t2",
        [["instance", "=", "pushgateway:9091"]],
        "t2",
        "prometheus",
        {"fixedColor": "blue", "mode": "fixed"},
    )
    assignment_fidelity = Metric(
        "assignment_fidelity",
        [["instance", "=", "pushgateway:9091"]],
        "assignment fidelity",
        "prometheus",
        {"fixedColor": "green", "mode": "fixed"},
    )
    assignment_fidelity = Metric(
        "assignment_fidelity",
        [["instance", "=", "pushgateway:9091"]],
        "assignment fidelity",
        "prometheus",
        {"fixedColor": "green", "mode": "fixed"},
    )
    assignment_fidelity_color_scale = Metric(
        "assignment_fidelity",
        [["instance", "=", "pushgateway:9091"]],
        "assignment fidelity",
        "prometheus",
        {
            "mode": "absolute",
            "steps": [
                {"color": "red", "value": None},
                {"value": 0.50, "color": "orange"},
                {"value": 0.80, "color": "green"},
            ],
        },
    )
    virtual_memory = Metric(
        "process_virtual_memory_bytes",
        [["instance", "=", "localhost:9090"]],
        "virtual memory",
        "prometheus",
        {"fixedColor": "blue", "mode": "fixed"},
    )
    resident_memory = Metric(
        "process_resident_memory_bytes",
        [["instance", "=", "localhost:9090"]],
        "resident memory",
        "prometheus",
        {"fixedColor": "red", "mode": "fixed"},
    )

    # create dashboard with timeseries plot
    dashboards = [
        {
            "title": "QPU Monitor",
            "panels": [
                {
                    "function": create_time_series,
                    "title": "",
                    "axis_label": "",
                    "metrics": [t1, t2],
                    "position": {
                        "x": 0,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "ns",
                },
                {
                    "function": create_stat,
                    "title": "Latest coherence times",
                    "metrics": [t1, t2],
                    "position": {
                        "x": 0,
                        "y": 0,
                        "w": 8,
                        "h": 2,
                    },
                    "unit": "ns",
                    "color_mode": "background_solid",
                    "color_steps": [
                        {
                            "color": "red",
                            "value": None,
                        },
                    ],
                },
                {
                    "function": create_time_series,
                    "title": "",
                    "axis_label": "",
                    "metrics": [assignment_fidelity],
                    "position": {
                        "x": 0,
                        "y": 10,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "percentunit",
                },
                {
                    "function": create_stat,
                    "title": "Latest assignment fidelity",
                    "metrics": [assignment_fidelity_color_scale],
                    "position": {
                        "x": 0,
                        "y": 8,
                        "w": 8,
                        "h": 2,
                    },
                    "unit": "percentunit",
                    "color_mode": "background_solid",
                    "color_steps": [
                        {
                            "color": "red",
                            "value": None,
                        },
                    ],
                },
                {
                    "function": create_time_series,
                    "title": "virtual memory",
                    "axis_label": "virtual memory",
                    "metrics": [virtual_memory, resident_memory],
                    "position": {
                        "x": 8,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "decbytes",
                },
                {
                    "function": create_stat,
                    "title": "latest virtual memory",
                    "metrics": [virtual_memory, resident_memory],
                    "position": {
                        "x": 8,
                        "y": 0,
                        "w": 8,
                        "h": 2,
                    },
                    "unit": "decbytes",
                    "color_mode": "background_solid",
                    "color_steps": [
                        {
                            "color": "blue",
                            "value": None,
                        },
                    ],
                },
            ],
        },
    ]
    for dashboard in dashboards:
        panels = []
        for panel in dashboard["panels"]:
            panels.append(panel["function"](panel))
        create_dashboard(dashboard, panels, HTTP_HEADERS)
