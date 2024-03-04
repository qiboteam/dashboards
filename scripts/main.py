from api_key import GRAFANA_KEY
from create_datasources import create_data_source
from create_dashboards import create_dashboard, create_stat, create_time_series


HTTP_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_KEY}", 
    "Accept": "application/json", 
    "Content-Type": "application/json",
}


if __name__ == "__main__":
    # create data sources
    data_sources = [
        {"name": "prometheus"}
    ]
    for data_source in data_sources:
        create_data_source(data_source, http_headers=HTTP_HEADERS)

    # create dashboard with timeseries plot
    dashboards = [
        {
            "title": "QPU Monitor",
            "panels": [
                {
                    "function": create_time_series,
                    "type": ["prometheus"],
                    "title": "cpu time",
                    "axis_label": "cpu time",
                    "metric": ["process_cpu_seconds_total"],
                    "legend": ["cpu seconds"],
                    "position": {
                        "x": 0,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "s",
                    "color": [{
                        "fixedColor": "purple",
                        "mode": "fixed",
                    }]
                },
                {
                    "function": create_stat,
                    "type": ["prometheus"],
                    "title": "latest cpu time",
                    "metric": ["process_cpu_seconds_total"],
                    "position": {
                        "x": 0,
                        "y": 0,
                        "w": 8,
                        "h": 2,
                    },
                    "unit": "s",
                    "color_mode": "background_solid",
                    "color_steps": [
                        {
                            "color": "purple",
                            "value": None,
                        },
                    ],
                },
                {
                    "function": create_time_series,
                    "type": ["prometheus", "prometheus"],
                    "title": "virtual memory",
                    "axis_label": "virtual memory",
                    "metric": ["process_virtual_memory_bytes", "process_resident_memory_bytes"],
                    "legend": ["virtual memory", "resident memory"],
                    "position": {
                        "x": 8,
                        "y": 2,
                        "w": 8,
                        "h": 6,
                    },
                    "unit": "decbytes",
                    "color": [{
                        "fixedColor": "blue",
                        "mode": "fixed",
                    },
                    {
                        "fixedColor": "red",
                        "mode": "fixed",
                    }]
                },
                {
                    "function": create_stat,
                    "type": ["prometheus", "prometheus"],
                    "title": "latest virtual memory",
                    "legend": ["virtual memory", "resident memory"],
                    "metric": ["process_virtual_memory_bytes", "process_resident_memory_bytes"],
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
