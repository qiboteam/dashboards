import requests
import json
from pathlib import Path

from utils import grafana_url


def create_data_source(data_source, http_headers):
    template_path = Path(__file__).parents[1] / "templates" / "new_datasource.json"

    datasource_template = json.loads(template_path.read_text())
    datasource_template["name"] = data_source["name"]
    requests.request("POST", grafana_url("datasources"), data=json.dumps(datasource_template), headers=http_headers)