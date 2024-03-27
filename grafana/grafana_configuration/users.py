import json

import requests

from .utils import grafana_url_authenticated


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
        f"{grafana_url_authenticated()}/admin/users",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
    if "role" in user_config:
        user_data = requests.get(
            f"{grafana_url_authenticated()}/users/lookup?loginOrEmail={user_config['login']}",
            data=json.dumps(user_config),
            headers={"Content-Type": "application/json"},
        ).text
        user_id = json.loads(user_data)["id"]
        requests.patch(
            f"{grafana_url_authenticated()}/orgs/1/users/{user_id}",
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
        f"{grafana_url_authenticated()}/admin/users/1/password",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
