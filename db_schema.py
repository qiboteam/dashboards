from typing import List, Tuple


import datetime as dt
from sqlalchemy import DateTime, ForeignKey, String, create_engine, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY


from config import db_address

engine = create_engine(db_address)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class QubitDevice(Base):
    """Table that holds general properties of qubit device.

    name (str): QPU name.
    nqubits (int): Number of qubits available.
    topology (List[Tuple[int]]): Array of integer pairs that denotes qubit-qubit connectivity. E.g. [(1, 2), (5, 6)]
    denotes connectivity between qubits 1 and 2, and qubits 5 and 6.
    """
    __tablename__ = "qpu_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    nqubits: Mapped[int]
    topology: Mapped[List[Tuple[int]]] = mapped_column(ARRAY(Integer, dimensions=2))

class CoherenceTime(Base):
    """Table that holds calibration measurements of the coherence time.

    qubit (int): ID of the qubit being measured.
    t1 (float): Decay time of the qubit excited state in nanoseconds.
    t2 (float): Dephasing time of the qubit in nanoseconds measured through a Ramsey experiment.
    t2_spin_echo (float): Dephasing time of the qubit in nanoseconds measured through a Hahn-echo experiment.
    """
    __tablename__ = "coherence_time_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    qubit: Mapped[int]
    t1: Mapped[float]
    t2: Mapped[float]
    t2_spin_echo: Mapped[float]
    datetime: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    qpu_id: Mapped[int] = mapped_column(ForeignKey("qpu_table.id"))

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
