from __future__ import annotations

from dataclasses import dataclass, field

import grafanalib.core as glc

from .group import Group
from .utils import DEFAULT_HEIGHT, DEFAULT_WIDTH


@dataclass
class Row:
    """Dashboard row, containing panels.

    Rows are a good way to organize panels in the dashboard, keeping panel order
    even if browser's window size changes (e.g. in mobile mode).
    Rows can be collapsed, hiding their panels.
    """

    title: str
    """Name of the row displayed in grafana."""
    x: int = 0
    y: int = 0
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    panels: list[glc.Panel] = field(default_factory=list)
    """List of grafana panels contained in the row."""

    @property
    def lowest_point(self) -> int:
        return max([self.y + self.height] + [p.lowest_point for p in self.panels])

    def add(self, panel):
        """Add panel to the row."""
        self.panels.append(panel)

    def add_group(self, group: Group):
        """Add all panels of the group to the row."""
        for p in group.panels:
            self.add(p)

    def below(self, other: Row) -> Row:
        """Place a new row below the other object."""
        shifted_group = self
        new_x = other.x
        new_y = other.lowest_point
        shifted_group.x = new_x
        shifted_group.y = new_y
        for i, _ in enumerate(shifted_group.panels):
            shifted_group.panels[i].y += new_y
        return shifted_group

    def to_json_data(self) -> dict:
        """Convert the row into a dictionary for grafana."""
        return {
            "gridPos": {
                "x": self.x,
                "y": self.y,
                "w": self.width,
                "h": self.height,
            },
            "id": None,
            "title": self.title,
            "type": "row",
        }
