"""Group of panels."""

from dataclasses import dataclass, field

from .panels import OverriddenPanel


@dataclass
class Group:
    panels: list[OverriddenPanel] = field(default_factory=list)
    x: int = 0
    y: int = 0

    @property
    def right_x(self):
        return max([p.right_x for p in self.panels])

    @property
    def lowest_point(self) -> int:
        return max([p.lowest_point for p in self.panels])
