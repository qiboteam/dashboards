"""Collect data from qibocal reports and upload them to prometheus."""

import json
from pathlib import Path

import yaml
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibocal.auto.serialize import deserialize


def from_path(json_path: Path):
    return json.loads(json_path.read_text())


def get_data(qibocal_output_folder: Path):
    platform = yaml.safe_load((qibocal_output_folder / "runcard.yml").read_text())[
        "platform"
    ]
    registry = CollectorRegistry()
    t1 = Gauge(f"{platform}_t1", f"T1 in us", registry=registry)
    t2 = Gauge(f"{platform}_t2", f"T2 in us", registry=registry)
    fidelity = Gauge(f"{platform}_assignment_fidelity", f"T2 in us", registry=registry)
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
        t1.set(path_t1["t1"][n][0])
        t2.set(path_t2["t2"][n][0])
        fidelity.set(path_fidelity["assignment_fidelity"][n])
    push_to_gateway("localhost:9091", job="pushgateway", registry=registry)


def export_metrics(qibocal_output_folder: Path):
    get_data(qibocal_output_folder)


if __name__ == "__main__":
    qibocal_output_folder = Path(__file__).parent.parent / "report"
    export_metrics(qibocal_output_folder)
