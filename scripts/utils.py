from pathlib import Path

import yaml


def grafana_port():
    compose_path = Path(__file__).parents[1] / "compose.yaml"
    print(compose_path)
    with open(compose_path) as f:
        compose_yaml = yaml.safe_load(f)
        return compose_yaml["services"]["grafana"]["ports"][0].split(":")[1]
    # return "3000"


def grafana_url(api_action):
    port = grafana_port()
    return f"http://grafana:{port}/api/{api_action}"
