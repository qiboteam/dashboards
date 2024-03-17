import requests
from grafana_configuration.scripts.utils import GRAFANA_CONTAINER_NAME, GRAFANA_PORT

headers = {
    "Content-Type": "application/json",
}

json_data = {
    "name": "setup_grafana",
    "role": "Admin",
}

response = requests.post(
    f"http://{GRAFANA_CONTAINER_NAME}:{GRAFANA_PORT}/api/serviceaccounts",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
account_id = response.json()["id"]

json_data = {
    "name": "setup_grafana-token",
}
response = requests.post(
    f"http://{GRAFANA_CONTAINER_NAME}:{GRAFANA_PORT}/api/serviceaccounts/{account_id}/tokens",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
GRAFANA_KEY = response.json()["key"]
"""API key for grafana."""
