import requests

from .utils import GRAFANA_URL

headers = {
    "Content-Type": "application/json",
}

json_data = {
    "name": "setup_grafana",
    "role": "Admin",
}

response = requests.post(
    f"{GRAFANA_URL}/serviceaccounts",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
account_id = response.json()["id"]

json_data = {
    "name": "setup_grafana-token",
}
response = requests.post(
    f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
GRAFANA_KEY = response.json()["key"]
"""API key for grafana."""
