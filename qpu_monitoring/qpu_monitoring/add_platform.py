from qibolab import create_platform
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from qpu_monitoring.database_schema import QPU
from qpu_monitoring.metrics_export import postgres_url


def add_platform(platform: str, qpu_name=None, **kwargs):
    """Adds a Qibolab platform to the Postgres DB"""
    if qpu_name is None:
        qpu_name = platform

    qibolab_platform = create_platform(platform)
    engine = create_engine(
        postgres_url(**kwargs),
        echo=True,
    )
    with Session(engine) as session:
        qpu = QPU(
            name=qpu_name,
            nqubits=qibolab_platform.nqubits,
            topology=[e for e in qibolab_platform.topology.edges],
        )
        session.add(qpu)
        session.commit()
