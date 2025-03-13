import argparse
import json
from pathlib import Path

from grafana_configuration import datasources
from grafana_configuration.templates.coherence_fidelity import (
    CoherenceFidelityDashboard,
)

from .api_key import grafana_key
from .users import change_admin_password, create_users
from .utils import DATASOURCE_CONFIGURATION_PATH

HTTP_HEADERS = {
    "Authorization": f"Bearer {grafana_key()}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
GRAFANA_TEMPLATES_PATH = Path(__file__).parent / "templates"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin", type=str, nargs="?", default=None)
    parser.add_argument("--users", type=str, nargs="?", default=None)
    parser.add_argument(
        "--qpu-config",
        type=Path,
        nargs="?",
        default=Path(__file__).parent / "config" / "qpu_config.json",
    )
    args = parser.parse_args()

    # create defined datasources
    data_sources = json.loads(DATASOURCE_CONFIGURATION_PATH.read_text())
    for data_source in data_sources:
        datasources.create(data_source, http_headers=HTTP_HEADERS)

    qpu_configuration = json.loads(args.qpu_config.read_text())
    for qpu_config in qpu_configuration["qpus"]:
        dash = CoherenceFidelityDashboard(
            title=qpu_config["name"], qubits=qpu_config["qubits"]
        )
        dash.create(http_headers=HTTP_HEADERS)

    if args.users is not None:
        user_configurations = json.loads(args.users)
        for user_configuration in user_configurations:
            create_users(user_configuration)
    if args.admin is not None:
        change_admin_password(args.admin)


if __name__ == "__main__":
    main()
