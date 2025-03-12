from dataclasses import dataclass, field

import grafanalib.core as glc

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
    x: int
    y: int
    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    panels: list[glc.Panel] = field(default_factory=list)
    """List of grafana panels contained in the row."""

    def add(self, panel):
        """Add panel to the row."""
        self.panels.append(panel)

    def to_json_data(self) -> dict:
        """Convert the row into a dictionary for grafana."""
        return {
            "grid_pos": {
                "x": self.x,
                "y": self.y,
                "w": self.width,
                "h": self.height,
            },
            "id": None,
            "title": self.title,
            "type": "row",
        }
