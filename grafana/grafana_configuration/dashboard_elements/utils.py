from dataclasses import dataclass

DEFAULT_WIDTH = 24
DEFAULT_HEIGHT = 1


@dataclass
class GridPos:
    x: int
    """Top left x position of the dashboard element."""
    y: int
    """Top left y position of the dashboard element."""
    w: int = DEFAULT_WIDTH
    """Width of the dashboard element (maximum is 24)."""
    h: int = DEFAULT_HEIGHT
    """Height of the dashboard element."""
