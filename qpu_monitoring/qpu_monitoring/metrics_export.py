"""Collect data from qibocal reports and upload them to prometheus."""

import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibocal.auto.serialize import deserialize
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .database_schema import Base, Qubit


def from_path(json_path: Path):
    return json.loads(json_path.read_text())


@dataclass
class QpuData:
    qubit_metrics: list[dict[str, Any]]
    acquisition_time: dt.datetime = field(default_factory=dt.datetime.now)


def get_data(qibocal_output_folder: Path) -> QpuData:
    qpu_data = []
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
        qubit_data = {
            "t1": path_t1["t1"][n][0],
            "t2": path_t2["t2"][n][0],
            "assignment_fidelity": path_fidelity["assignment_fidelity"][n],
        }
        qpu_data.append(qubit_data)
    report_meta = json.loads((qibocal_output_folder / "meta.json").read_text())
    date = report_meta["date"]
    time = report_meta["start-time"]
    acquisition_time = dt.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    return QpuData(qpu_data, acquisition_time)


def push_data_prometheus(platform: str, qpu_data: QpuData):
    registry = CollectorRegistry()
    registry_gauges = {}
    for key in qpu_data.qubit_metrics[0]:
        gauge = Gauge(f"{platform}_{key}", f"{platform}_{key}", registry=registry)
        registry_gauges[key] = gauge

    for qubit_data in qpu_data.qubit_metrics:
        for key, value in qubit_data.items():
            registry_gauges[key].set(value)
    push_to_gateway("localhost:9091", job="pushgateway", registry=registry)


def postgres_url(
    username: str, password: str, container: str, port: int, database: str
) -> str:
    """Connection url to PostgreSQL database."""
    return f"postgresql+psycopg2://{username}:{password}@{container}:{port}/{database}"


def push_data_postgres(platform: str, qpu_data: QpuData, **kwargs):
    engine = create_engine(
        postgres_url(**kwargs),
        echo=True,
    )
    Base.metadata.create_all(engine)

    for i, qubit_data in enumerate(qpu_data.qubit_metrics):
        with Session(engine) as session:
            qubit = Qubit(
                qubit_id=i,
                qpu_name=platform,
                acquisition_time=qpu_data.acquisition_time,
                **qubit_data,
            )

            session.add_all([qubit])

            session.commit()


def export_metrics(
    qibocal_output_folder: Path, export_database: str = "pushgateway", **kwargs
):
    platform = yaml.safe_load((qibocal_output_folder / "runcard.yml").read_text())[
        "platform"
    ]
    qpu_data = get_data(qibocal_output_folder)
    if export_database == "pushgateway":
        push_data_prometheus(platform, qpu_data)
    elif export_database == "postgres":
        push_data_postgres(platform, qpu_data, **kwargs)
    else:
        raise NotImplementedError
