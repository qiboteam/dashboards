"""qibocal-csv-monitor.py
Generates a JSON index with reports information.
"""

import json
import sys

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibocal.auto.serialize import deserialize

# configuration = {
#     'qm_tests': 1
# }

ROOT = "/nfs/users/qibocal/monitor/%s"


def from_path(p, path):
    json_meta = p / path
    json_res = {}
    if json_meta.exists():
        with json_meta.open() as f:
            try:
                json_res = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(f"Error processing {json_meta}: {e}", file=sys.stderr)
    # return deserialize(json_res)
    return json_res


from pathlib import Path
from random import random

registry = CollectorRegistry()
t1 = Gauge(f"t1", f"T1 in us", registry=registry)
t2 = Gauge(f"t2", f"T2 in us", registry=registry)
fidelity = Gauge(f"assignment_fidelity", f"T2 in us", registry=registry)


def get_data():
    qibocal_output_folder = Path(__file__).parent / "report"
    for n in range(1):
        path_t1 = deserialize(
            from_path(qibocal_output_folder, f"data/t1_{n}/results.json")
        )
        path_t2 = deserialize(
            from_path(qibocal_output_folder, f"data/t2_{n}/results.json")
        )
        path_fidelity = deserialize(
            from_path(
                qibocal_output_folder, f"data/readout characterization_{n}/results.json"
            )
        )
        t1.set(path_t1["t1"][n])
        t2.set(path_t2["t2"][n])
        fidelity.set(path_fidelity["assignment_fidelity"][n] + 0.4)
    push_to_gateway("pushgateway:9091", job="pushgateway", registry=registry)


if __name__ == "__main__":
    get_data()
