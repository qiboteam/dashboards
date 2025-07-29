"""Dashboard used by the coherence-fidelity template."""

from typing import Optional

from grafana_configuration.dashboard_elements.group import Group
from grafana_configuration.dashboard_elements.metric import Metric
from grafana_configuration.dashboard_elements.panels import Stat, TimeSeries
from grafana_configuration.dashboard_elements.row import Row
from grafana_configuration.dashboards import Dashboard

from .group import CoherenceFidelityGroup


class CoherenceFidelityDashboard(Dashboard):
    def __init__(
        self,
        *args,
        title: str = "",
        qubits: Optional[list] = None,
        timezone: str = "browser",
        **kwargs,
    ):
        """Create an empty dashboard.

        Args:
            timezone (str): timezone used by plots.
                supported values: "browser", "utc" (default for grafanalib),
                "" (default for grafana), region/city or region/state/city
        """
        super().__init__(*args, title=title, timezone=timezone, **kwargs)
        if qubits is None:
            qubits = []
        self.qubits = qubits

        coherence_row = Row(title="Coherence times")
        previous = coherence_row
        for qubit in self.qubits:
            coherence_metrics = [
                Metric(name="t1", color="red", qpu_name=self.title, qubit_id=qubit),
                Metric(name="t2", color="blue", qpu_name=self.title, qubit_id=qubit),
            ]
            group = CoherenceFidelityGroup(
                metrics=coherence_metrics,
                title=f"Qubit {qubit}",
                unit="ns",
            ).right_of(previous)
            previous = group
            coherence_row.add_group(group)
        self.add_row(coherence_row)

        fidelity_row = Row(title="Fidelities").below(coherence_row)
        previous = fidelity_row
        for qubit in self.qubits:
            fidelity_metrics = [
                Metric(
                    name="assignment_fidelity",
                    color="green",
                    qpu_name=self.title,
                    qubit_id=qubit,
                ),
            ]
            group = CoherenceFidelityGroup(
                metrics=fidelity_metrics,
                title=f"Qubit {qubit}",
                unit="percentunit",
                axis_soft_max=1,
            ).right_of(previous)
            previous = group
            fidelity_row.add_group(group)
        self.add_row(fidelity_row)

    @classmethod
    def from_qpu_config(cls, config: dict):
        return cls(title=config["name"], qubits=config["qubits"])
