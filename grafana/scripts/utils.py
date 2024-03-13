GRAFANA_PORT = "3000"
"""Port of grafana defined in compose.yaml"""
GRAFANA_CONTAINER_NAME = "grafana"
"""Name of the grafana container defined in compose.yaml"""


def grafana_url(api_action: str) -> str:
    """Url of the api for the grafana container."""
    return f"http://{GRAFANA_CONTAINER_NAME}:{GRAFANA_PORT}/api/{api_action}"
