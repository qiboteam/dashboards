from dataclasses import dataclass


@dataclass
class GridPos:
    x: int
    y: int
    w: int = 24
    h: int = 1
