import json
from pathlib import Path

from grafana_configuration.scripts import datasources
from grafana_configuration.scripts.api_key import GRAFANA_KEY

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
