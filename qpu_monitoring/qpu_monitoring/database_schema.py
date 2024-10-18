import datetime as dt
from typing import List, Tuple

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class QPU(Base):
    __tablename__ = "qpu"

    id: Mapped[int] = mapped_column(primary_key=True)
    """Primary key."""
    name: Mapped[str] = mapped_column(String(50), unique=True)
    """Platform name"""
    nqubits: Mapped[int]
    """Number of qubits for chip"""
    topology: Mapped[List[Tuple[int]]] = mapped_column(ARRAY(Integer, dimensions=2))
    """QPU topology"""


class BaseCharacterizationData(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    """Primary key."""
    qubit_id: Mapped[int]
    """Qubit id."""
    qpu_id: Mapped[int] = mapped_column(ForeignKey("qpu.id"))
    """QPU id."""

    @declared_attr
    def qpu(self):
        return relationship("QPU")

    """QPU object"""
    acquisition_time: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    """Time when metrics are acquired."""

    @declared_attr
    def __mapper_args__(cls):
        if cls.__name__ == "BaseCharacterizationData":
            return {
                "polymorphic_identity": "BaseCharacterizationData",
                "polymorphic_on": cls.type,
            }
        else:
            return {"polymorphic_identity": cls.__name__}

    def __str__(self) -> str:
        return f"Qubit(id={self.id}, qubit_id={self.qubit_id}, qpu_name={self.qpu.name}, time={self.acquisition_time})"


class CoherenceTime(BaseCharacterizationData):
    __tablename__ = "coherence_time"

    t1: Mapped[float]
    """Qubit t1 in ns."""
    t2: Mapped[float]
    """Qubit t2 in ns."""
    # t2_spin_echo: Mapped[float]
    # """Qubit t2 spin echo in ns."""


class AssignmentFidelity(BaseCharacterizationData):
    __tablename__ = "assignment_fidelity"

    assignment_fidelity: Mapped[float]
    """Qubit assignment fidelity in the range [0,1]."""
