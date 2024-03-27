import json

import requests

from .utils import GRAFANA_URL_AUTHENTICATED


def create_users(user_config: dict[str, str]):
    """Create grafana users.

    Example of user_config
    ```
    {
        "login": "username",
        "password": "password",
        "role": "Editor",  # (one of Admin, Editor, Viewer) (optional)
    },
    ```
    Args:
        user_config (dict[str, str]): usernames, passwords
            and permissions of users to be created.
    """
    requests.post(
        f"{GRAFANA_URL_AUTHENTICATED}/admin/users",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
    if "role" in user_config:
        user_data = requests.get(
            f"{GRAFANA_URL_AUTHENTICATED}/users/lookup?loginOrEmail={user_config['login']}",
            data=json.dumps(user_config),
            headers={"Content-Type": "application/json"},
        ).text
        user_id = json.loads(user_data)["id"]
        requests.patch(
            f"{GRAFANA_URL_AUTHENTICATED}/orgs/1/users/{user_id}",
            data=json.dumps(user_config),
            headers={"Content-Type": "application/json"},
        )


def change_admin_password(new_password: str):
    """Set a new password for the grafana admin user.

    Args:
        new_password (str): new password for the grafana admin user.
    """
    user_config = {"password": new_password}
    requests.put(
        f"{GRAFANA_URL_AUTHENTICATED}/admin/users/1/password",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
