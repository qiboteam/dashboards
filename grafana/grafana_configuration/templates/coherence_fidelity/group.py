from dataclasses import dataclass, field

from grafana_configuration.dashboard_elements.group import Group
from grafana_configuration.dashboard_elements.metric import Metric
from grafana_configuration.dashboard_elements.panels import Stat, TimeSeries

STAT_PANEL_SIZE = {"width": 5, "height": 2}
TIMESERIES_PANEL_SIZE = {"width": 5, "height": 6}


@dataclass
class CoherenceFidelityGroup(Group):
    metrics: list[Metric] = field(default_factory=list)
    title: str = ""

    def __post_init__(self):
        stat_panel = Stat(
            unit="ns",
            x=self.x,
            y=self.y,
            **STAT_PANEL_SIZE,
            title=self.title,
            targets=[p.to_target() for p in self.metrics],
        )
        timeseries_panel = TimeSeries(
            unit="ns",
            **TIMESERIES_PANEL_SIZE,
            title=self.title,
            targets=[p.to_target() for p in self.metrics],
        ).below(stat_panel)
        self.panels.extend([stat_panel, timeseries_panel])
