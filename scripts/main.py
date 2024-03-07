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


if __name__ == "__main__":
    # create data sources
    data_sources = [{"name": "prometheus"}]
    for data_source in data_sources:
        create_data_source(data_source, http_headers=HTTP_HEADERS)

    # create dashboard with timeseries plot
    dashboards = [
        {
            "title": "QPU Monitor",
            "panels": [
                {
                    "function": create_time_series,
                    "type": ["prometheus", "prometheus"],
                    "title": "",
                    "axis_label": "",
                    "metric": ["t1", "t2"],
                    "label_filters": [
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                    ],
                    "legend": ["t1", "t2"],
                    "position": {
                        "x": 0,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "ns",
                    "color": [
                        {
                            "fixedColor": "red",
                            "mode": "fixed",
                        },
                        {
                            "fixedColor": "blue",
                            "mode": "fixed",
                        },
                    ],
                },
                {
                    "function": create_stat,
                    "type": ["prometheus", "prometheus"],
                    "title": "Latest coherence times",
                    "metric": ["t1", "t2"],
                    "label_filters": [
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                    ],
                    "legend": ["t1", "t2"],
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
                    "color": [
                        {
                            "fixedColor": "red",
                            "mode": "fixed",
                        },
                        {
                            "fixedColor": "blue",
                            "mode": "fixed",
                        },
                    ],
                },
                {
                    "function": create_time_series,
                    "type": ["prometheus"],
                    "title": "",
                    "axis_label": "",
                    "metric": ["assignment_fidelity"],
                    "label_filters": [
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                    ],
                    "legend": ["assignment fidelity"],
                    "position": {
                        "x": 0,
                        "y": 10,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "percentunit",
                    "color": [
                        {
                            "fixedColor": "green",
                            "mode": "fixed",
                        }
                    ],
                },
                {
                    "function": create_stat,
                    "type": ["prometheus"],
                    "title": "Latest assignment fidelity",
                    "metric": ["assignment_fidelity"],
                    "label_filters": [
                        [
                            ["instance", "=", "pushgateway:9091"],
                        ],
                    ],
                    "legend": ["assignment fidelity"],
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
                    "color": [
                        {
                            "mode": "absolute",
                            "steps": [
                                {"color": "red", "value": None},
                                {"value": 0.50, "color": "orange"},
                                {"value": 0.80, "color": "green"},
                            ],
                        }
                    ],
                },
                {
                    "function": create_time_series,
                    "type": ["prometheus", "prometheus"],
                    "title": "virtual memory",
                    "axis_label": "virtual memory",
                    "metric": [
                        "process_virtual_memory_bytes",
                        "process_resident_memory_bytes",
                    ],
                    "label_filters": [
                        [
                            ["instance", "=", "localhost:9090"],
                        ],
                        [
                            ["instance", "=", "localhost:9090"],
                        ],
                    ],
                    "legend": ["virtual memory", "resident memory"],
                    "position": {
                        "x": 8,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "decbytes",
                    "color": [
                        {
                            "fixedColor": "blue",
                            "mode": "fixed",
                        },
                        {
                            "fixedColor": "red",
                            "mode": "fixed",
                        },
                    ],
                },
                {
                    "function": create_stat,
                    "type": ["prometheus", "prometheus"],
                    "title": "latest virtual memory",
                    "legend": ["virtual memory", "resident memory"],
                    "metric": [
                        "process_virtual_memory_bytes",
                        "process_resident_memory_bytes",
                    ],
                    "label_filters": [
                        [
                            ["instance", "=", "localhost:9090"],
                        ],
                        [
                            ["instance", "=", "localhost:9090"],
                        ],
                    ],
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
                    "color": [
                        {
                            "fixedColor": "blue",
                            "mode": "fixed",
                        },
                        {
                            "fixedColor": "red",
                            "mode": "fixed",
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
