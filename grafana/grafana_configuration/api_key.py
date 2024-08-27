import requests

from .utils import ADMIN_PASSWORD, ADMIN_USERNAME, GRAFANA_URL

API_CREATION_HTTP_HEADERS = {
    "Content-Type": "application/json",
}


def find_admin_account_id() -> int:
    """Account id of the user named "admin"."""
    admin_id_json_data = {
        "name": "setup_grafana",
        "role": "Admin",
    }
    try:
        response = requests.get(
            f"{GRAFANA_URL}/serviceaccounts/search?query=setup_grafana",
            headers=API_CREATION_HTTP_HEADERS,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        return response.json()["serviceAccounts"][0]["id"]
    except:
        response = requests.post(
            f"{GRAFANA_URL}/serviceaccounts",
            headers=API_CREATION_HTTP_HEADERS,
            json=admin_id_json_data,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        return response.json()["id"]


def grafana_key() -> str:
    """API key for grafana."""
    account_id = find_admin_account_id()

    # create a token for the admin id found
    token_json_data = {
        "name": "setup_grafana-token",
    }
    try:
        get_token_response = requests.get(
            f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens",
            headers=API_CREATION_HTTP_HEADERS,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        token_id = get_token_response.json()[0]["id"]
        delete_response = requests.delete(
            f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens/{token_id}",
            headers=API_CREATION_HTTP_HEADERS,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        response_2 = requests.post(
            f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens",
            headers=API_CREATION_HTTP_HEADERS,
            json=token_json_data,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        return response_2.json()["key"]
    except:
        response = requests.post(
            f"{GRAFANA_URL}/serviceaccounts/{account_id}/tokens",
            headers=API_CREATION_HTTP_HEADERS,
            json=token_json_data,
            auth=(ADMIN_USERNAME, ADMIN_PASSWORD),
        )
        return response.json()["key"]
