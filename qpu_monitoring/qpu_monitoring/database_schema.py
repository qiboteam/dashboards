import datetime as dt

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


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
