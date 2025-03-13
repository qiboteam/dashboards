"""Dashboard used by the coherence-fidelity template."""

from typing import Optional

from grafana_configuration.dashboard_elements.group import Group
from grafana_configuration.dashboard_elements.metric import Metric
from grafana_configuration.dashboard_elements.panels import Stat, TimeSeries
from grafana_configuration.dashboard_elements.row import Row
from grafana_configuration.dashboards import Dashboard


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

        stat_panel_size = {"width": 5, "height": 2}
        timeseries_panel_size = {"width": 5, "height": 6}

        coherence_row = Row(title="Coherence times", x=0, y=0)
        start_group_pos = below(coherence_row)
        for qubit in self.qubits:
            coherence_metrics = [
                Metric(name="t1", color="red", qpu_name=self.title, qubit_id=qubit),
                Metric(name="t2", color="blue", qpu_name=self.title, qubit_id=qubit),
            ]
            stat_panel = Stat(
                unit="ns",
                **start_group_pos,
                **stat_panel_size,
                title=f"Qubit {qubit}",
                targets=[p.to_target() for p in coherence_metrics],
            )
            timeseries_panel = TimeSeries(
                unit="ns",
                **timeseries_panel_size,
                title=f"Qubit {qubit}",
                targets=[p.to_target() for p in coherence_metrics],
            ).below(stat_panel)
            group = Group([stat_panel, timeseries_panel])
            start_group_pos = right_of(group)
            coherence_row.add_group(group)
        self.add_row(coherence_row)

        fidelity_row = Row(title="Fidelities", **below(coherence_row))
        start_group_pos = below(fidelity_row)
        for qubit in self.qubits:
            fidelity_metrics = [
                Metric(
                    name="assignment_fidelity",
                    color="green",
                    qpu_name=self.title,
                    qubit_id=qubit,
                ),
            ]
            stat_panel = Stat(
                unit="percentunit",
                **start_group_pos,
                **stat_panel_size,
                title=f"Qubit {qubit}",
                targets=[p.to_target() for p in fidelity_metrics],
            )
            timeseries_panel = TimeSeries(
                unit="percentunit",
                **timeseries_panel_size,
                title=f"Qubit {qubit}",
                targets=[p.to_target() for p in fidelity_metrics],
            ).below(stat_panel)
            group = Group([stat_panel, timeseries_panel])
            start_group_pos = right_of(group)
            fidelity_row.add_group(group)
        self.add_row(fidelity_row)

    @classmethod
    def from_qpu_config(cls, config: dict):
        return cls(title=config["name"], qubits=config["qubits"])


def right_of(dashboard_element):
    new_x = dashboard_element.right_x
    if new_x + 5 > 24:  # ???
        return {"x": 0, "y": dashboard_element.lowest_point}  # ???
    return {"x": new_x, "y": dashboard_element.y}


def below(dashboard_element):
    return {"x": dashboard_element.x, "y": dashboard_element.lowest_point}
