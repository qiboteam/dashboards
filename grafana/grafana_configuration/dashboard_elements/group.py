"""Group of panels."""

from dataclasses import dataclass, field

from .panels import OverriddenPanel


@dataclass
class Group:
    panels: list[OverriddenPanel] = field(default_factory=list)

    @property
    def x(self):
        return self.panels[0].x if self.panels else 0

    @property
    def y(self):
        return self.panels[0].y if self.panels else 0

    @property
    def right_x(self):
        return max([p.right_x for p in self.panels])

    @property
    def lowest_point(self) -> int:
        return max([p.lowest_point for p in self.panels])
