"""Collect data from qibocal reports and upload them to prometheus."""

import collections
import datetime as dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from qibocal.auto.output import Output
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .database_schema import Base, Qubit
from .experiments import METRICS


@dataclass
class QpuData:
    qubit_metrics: dict[str, dict[str, Any]]
    """Dictionary of metrics acquired using qibocal.
    Its outermost key is the qubit id. For each qubit, it stores
    a dictionary with acquired data."""
    acquisition_time: dt.datetime = field(default_factory=dt.datetime.now)
    """Date and time of the qibocal acquisition."""


def get_data(qibocal_output_folder: Path) -> QpuData:
    """Read metrics acquired by qibocal from the report."""
    out = Output.load(qibocal_output_folder)
    report_meta = out.meta
    acquisition_time = report_meta.start_time
    qpu_data = collections.defaultdict(dict)

    for task_id, result in out.history.items():
        task_id = task_id.id
        metric = METRICS[task_id]

        metric_values = getattr(result.results, metric)
        for qubit_id, qubit_metric in metric_values.items():
            if isinstance(qubit_metric, list):
                qubit_metric = qubit_metric[0]
            qpu_data[qubit_id][metric] = qubit_metric
    return QpuData(qpu_data, acquisition_time)


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

    for qubit_id, qubit_data in qpu_data.qubit_metrics.items():
        with Session(engine) as session:
            qubit = Qubit(
                qubit_id=qubit_id,
                qpu_name=platform,
                acquisition_time=qpu_data.acquisition_time,
                **qubit_data,
            )
            session.add_all([qubit])
            session.commit()


def export_metrics(
    qibocal_output_folder: Path, export_database: str = "pushgateway", **kwargs
):
    platform = json.loads((qibocal_output_folder / "meta.json").read_text())["platform"]
    qpu_data = get_data(qibocal_output_folder)
    if export_database == "postgres":
        push_data_postgres(platform, qpu_data, **kwargs)
    else:
        raise NotImplementedError
