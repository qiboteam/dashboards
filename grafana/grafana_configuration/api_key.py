import requests

from .utils import GRAFANA_URL

API_CREATION_HTTP_HEADERS = {
    "Content-Type": "application/json",
}


def find_admin_account_id() -> int:
    """Account id of the user named "admin"."""
    admin_id_json_data = {
        "name": "setup_grafana",
        "role": "Admin",
    }
    response = requests.post(
        f"{GRAFANA_URL}/serviceaccounts",
        headers=API_CREATION_HTTP_HEADERS,
        json=admin_id_json_data,
        auth=("admin", "admin"),
    )
    return response.json()["id"]


def grafana_key() -> str:
    """API key for grafana."""
    account_id = find_admin_account_id()

    # create a token for the admin id found
    token_json_data = {
        "name": "setup_grafana-token",
    }
    response = requests.post(
        f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens",
        headers=API_CREATION_HTTP_HEADERS,
        json=token_json_data,
        auth=("admin", "admin"),
    )
    return response.json()["key"]
