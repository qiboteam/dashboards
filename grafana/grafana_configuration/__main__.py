import json
from pathlib import Path

from grafana_configuration import datasources

from .api_key import GRAFANA_KEY
from .users import change_admin_password, create_users

HTTP_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


if __name__ == "__main__":
    # create defined datasources
    datasource_configuration_path = (
        Path(__file__).parent / "config" / "datasources.json"
    )
    data_sources = json.loads(datasource_configuration_path.read_text())
    for data_source in data_sources:
        datasources.create(data_source, http_headers=HTTP_HEADERS)

    # configuration files for all users can be saved in separate files (e.g. json)
    user_configurations = [
        {
            "login": "newuser",
            "password": "newpassword",
        },
    ]
    # it cannot be explicitly exposed in python
    admin_password = "123456"
    for user_configuration in user_configurations:
        create_users(user_configuration)
    change_admin_password(admin_password)
