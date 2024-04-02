"""Collect data from qibocal reports and upload them to prometheus."""

import json
from pathlib import Path

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibocal.auto.serialize import deserialize


def from_path(json_path):
    return json.loads(json_path.read_text())


def get_data():
    qibocal_output_folder = Path(__file__).parent.parent / "report"
    for n in range(1):
        path_t1 = deserialize(
            from_path(qibocal_output_folder / "data" / f"t1_{n}" / "results.json")
        )
        path_t2 = deserialize(
            from_path(qibocal_output_folder / "data" / f"t2_{n}" / "results.json")
        )
        path_fidelity = deserialize(
            from_path(
                qibocal_output_folder
                / "data"
                / f"readout characterization_{n}"
                / "results.json"
            )
        )
        t1.set(path_t1["t1"][n])
        t2.set(path_t2["t2"][n])
        fidelity.set(path_fidelity["assignment_fidelity"][n])
    push_to_gateway("pushgateway:9091", job="pushgateway", registry=registry)


if __name__ == "__main__":
    registry = CollectorRegistry()
    t1 = Gauge(f"t1", f"T1 in us", registry=registry)
    t2 = Gauge(f"t2", f"T2 in us", registry=registry)
    fidelity = Gauge(f"assignment_fidelity", f"T2 in us", registry=registry)
    get_data()
