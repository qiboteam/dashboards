import requests
from utils import grafana_port

headers = {
    "Content-Type": "application/json",
}

json_data = {
    "name": "test",
    "role": "Admin",
}

response = requests.post(
    f"http://grafana:{grafana_port()}/api/serviceaccounts",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
account_id = response.json()["id"]

json_data = {
    "name": "test-token",
}
response = requests.post(
    f"http://grafana:{grafana_port()}/api/serviceaccounts/{account_id}/tokens",
    headers=headers,
    json=json_data,
    auth=("admin", "admin"),
)
GRAFANA_KEY = response.json()["key"]  # to be saved in environment variables
