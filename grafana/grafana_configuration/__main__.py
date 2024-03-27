import argparse
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin", type=str, nargs="?", default=None)
    parser.add_argument("--users", type=str, nargs="?", default=None)
    args = parser.parse_args()

    # create defined datasources
    datasource_configuration_path = (
        Path(__file__).parent / "config" / "datasources.json"
    )
    data_sources = json.loads(datasource_configuration_path.read_text())
    for data_source in data_sources:
        datasources.create(data_source, http_headers=HTTP_HEADERS)

    if args.users is not None:
        user_configurations = json.loads(args.users)
        for user_configuration in user_configurations:
            create_users(user_configuration)
    if args.admin is not None:
        change_admin_password(args.admin)


if __name__ == "__main__":
    main()
