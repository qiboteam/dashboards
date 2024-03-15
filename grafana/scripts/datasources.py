import json
from pathlib import Path

import requests
from utils import grafana_url


def create(data_source: dict[str, str], http_headers: dict[str, str]):
    """Create a new datasource.

    Args:
        data_source (dict[str, str]): overridden values of the new datasource.
        http_headers (dict[str, str]): http headers for the request containing the API key.
    """
    template_path = Path(__file__).parents[1] / "templates" / "datasource.json"

    datasource_template = json.loads(template_path.read_text())
    for key, value in data_source.items():
        datasource_template[key] = value
    requests.request(
        "POST",
        grafana_url("datasources"),
        data=json.dumps(datasource_template),
        headers=http_headers,
    )
