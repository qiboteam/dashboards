import argparse
import json

from grafana_configuration import dashboards, datasources

from .api_key import grafana_key
from .users import change_admin_password, create_users
from .utils import DASHBOARD_CONFIGURATION_PATH, DATASOURCE_CONFIGURATION_PATH

HTTP_HEADERS = {
    "Authorization": f"Bearer {grafana_key()}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin", type=str, nargs="?", default=None)
    parser.add_argument("--users", type=str, nargs="?", default=None)
    args = parser.parse_args()

    # create defined datasources
    data_sources = json.loads(DATASOURCE_CONFIGURATION_PATH.read_text())
    for data_source in data_sources:
        datasources.create(data_source, http_headers=HTTP_HEADERS)

    dashboards_configurations = json.loads(DASHBOARD_CONFIGURATION_PATH.read_text())
    for dashboards_configuration in dashboards_configurations:
        dashboards.create(dashboards_configuration, http_headers=HTTP_HEADERS)

    if args.users is not None:
        user_configurations = json.loads(args.users)
        for user_configuration in user_configurations:
            create_users(user_configuration)
    if args.admin is not None:
        change_admin_password(args.admin)


if __name__ == "__main__":
    main()
