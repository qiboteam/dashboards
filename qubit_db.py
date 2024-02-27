from typing import List


import datetime as dt
from sqlalchemy import DateTime, ForeignKey, String, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


from config import db_address

engine = create_engine(db_address)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Qubit(Base):
    __tablename__ = "qubit_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    t1: Mapped[float]
    t2: Mapped[float]
    t2_spin_echo: Mapped[float]
    assignment_fidelity: Mapped[float]
    readout_fidelity: Mapped[float]
    gate_fidelity: Mapped[float]
    datetime: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    chip_id: Mapped[int] = mapped_column(ForeignKey("qubit_chip_table.id"))

class QubitPair(Base):
    __tablename__ = "qubit_pair_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    chip_id: Mapped[int] = mapped_column(ForeignKey("qubit_chip_table.id"))
    gate_type: Mapped[str] = mapped_column(String(5))
    gate_fidelity: Mapped[float]
    qubit1: Mapped[int]
    qubit2: Mapped[int]

class QubitChip(Base):
    __tablename__ = "qubit_chip_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    qubits: Mapped[List[Qubit]] = relationship()
    mapping: Mapped[List[QubitPair]] = relationship()
    datetime: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
