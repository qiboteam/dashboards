"""Collect data from qibocal reports and upload them to prometheus."""

import datetime as dt
import json
from pathlib import Path
from typing import Any

import yaml
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibocal.auto.serialize import deserialize
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.sql import func


def from_path(json_path: Path):
    return json.loads(json_path.read_text())


class Base(DeclarativeBase):
    pass


class Qubit(Base):
    __tablename__ = "qubit"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Primary key."""
    qubit_id: Mapped[int]
    """Qubit id."""
    qpu_name: Mapped[str]
    """QPU name."""
    t1: Mapped[float]
    """Qubit t1 in ns."""
    t2: Mapped[float]
    """Qubit t2 in ns."""
    # t2_spin_echo: Mapped[float]
    # """Qubit t2 spin echo in ns."""
    assignment_fidelity: Mapped[float]
    """Qubit assignment fidelity in the range [0,1]."""
    acquisition_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    """Time when metrics are acquired."""

    def __repr__(self) -> str:
        return f"Qubit(id={self.id}, qubit_id={self.qubit_id}, qpu_name={self.qpu_name}, time={self.acquisition_time})"


def get_data(qibocal_output_folder: Path) -> list[dict[str, Any]]:
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
    return qpu_data


def push_data_prometheus(platform: str, qpu_data: list[dict[str, Any]]):
    registry = CollectorRegistry()
    registry_gauges = {}
    for key in qpu_data[0].keys():
        gauge = Gauge(f"{platform}_{key}", f"{platform}_{key}", registry=registry)
        registry_gauges[key] = gauge

    for qubit_data in qpu_data:
        for key, value in qubit_data.items():
            registry_gauges[key].set(value)
    push_to_gateway("localhost:9091", job="pushgateway", registry=registry)


def push_data_postgres(platform: str, qpu_data: list[dict[str, Any]]):
    engine = create_engine(
        "postgresql+psycopg2://dash_admin:dash_admin@postgres:5432/qpu_metrics",
        echo=True,
    )
    Base.metadata.create_all(engine)

    for i, qubit_data in enumerate(qpu_data):
        with Session(engine) as session:
            qubit = Qubit(
                qubit_id=i,
                qpu_name=platform,
                **qubit_data,
            )

            session.add_all([qubit])

            session.commit()


def export_metrics(qibocal_output_folder: Path, export_database: str = "pushgateway"):
    platform = yaml.safe_load((qibocal_output_folder / "runcard.yml").read_text())[
        "platform"
    ]
    qpu_data = get_data(qibocal_output_folder)
    if export_database == "pushgateway":
        push_data_prometheus(platform, qpu_data)
    elif export_database == "postgres":
        push_data_postgres(platform, qpu_data)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    qibocal_output_folder = Path(__file__).parent.parent / "report"
    export_metrics(qibocal_output_folder)
