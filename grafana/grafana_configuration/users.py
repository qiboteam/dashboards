import json

import requests


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
    from .utils import grafana_url

    requests.request(
        "POST",
        "http://admin:admin@grafana:3000/api/admin/users",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
    if "role" in user_config:
        user_data = requests.request(
            "GET",
            f"http://admin:admin@grafana:3000/api/users/lookup?loginOrEmail={user_config['login']}",
            data=json.dumps(user_config),
            headers={"Content-Type": "application/json"},
        ).text
        user_id = json.loads(user_data)["id"]
        requests.request(
            "PATCH",
            f"http://admin:admin@grafana:3000/api/orgs/1/users/{user_id}",
            data=json.dumps(user_config),
            headers={"Content-Type": "application/json"},
        )


def change_admin_password(new_password: str):
    """Set a new password for the grafana admin user.

    Args:
        new_password (str): new password for the grafana admin user.
    """
    user_config = {"password": new_password}
    requests.request(
        "PUT",
        "http://admin:admin@grafana:3000/api/admin/users/1/password",
        data=json.dumps(user_config),
        headers={"Content-Type": "application/json"},
    )
