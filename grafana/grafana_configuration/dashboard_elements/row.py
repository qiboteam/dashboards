from dataclasses import dataclass

from .utils import GridPos


@dataclass
class Row:
    """Dashboard row, containing panels."""

    title: str
    """Name of the row displayed in grafana."""
    grid_pos: GridPos
    """xy position of the row in the dashboard (width and height default to (24,1))."""

    def to_json_data(self) -> dict:
        """Convert the row into a dictionary for grafana."""
        return {
            "gridPos": self.grid_pos.__dict__,
            "id": None,
            "title": self.title,
            "type": "row",
        }
