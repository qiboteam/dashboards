from dataclasses import dataclass, field

import grafanalib.core as glc

from .utils import GridPos


@dataclass
class Row:
    """Dashboard row, containing panels.

    Rows are a good way to organize panels in the dashboard, keeping panel order
    even if browser's window size changes (e.g. in mobile mode).
    Rows can be collapsed, hiding their panels.
    """

    title: str
    """Name of the row displayed in grafana."""
    grid_pos: GridPos
    """xy position of the row in the dashboard (width and height default to (24,1))."""
    panels: list[glc.Panel] = field(default_factory=list)
    """List of grafana panels contained in the row."""

    def add(self, panel):
        """Add panel to the row."""
        self.panels.append(panel)

    def to_json_data(self) -> dict:
        """Convert the row into a dictionary for grafana."""
        return {
            "gridPos": self.grid_pos.__dict__,
            "id": None,
            "title": self.title,
            "type": "row",
        }
