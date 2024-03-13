import json
from pathlib import Path

from api_key import GRAFANA_KEY
from create_datasources import create_datasource

HTTP_HEADERS = {
    "Authorization": f"Bearer {GRAFANA_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


if __name__ == "__main__":
    # create defined datasources
    datasource_configuration_path = (
        Path(__file__).parents[1] / "config" / "datasources.json"
    )
    data_sources = json.loads(datasource_configuration_path.read_text())
    for data_source in data_sources:
        create_datasource(data_source, http_headers=HTTP_HEADERS)
