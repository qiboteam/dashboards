"""Group of panels."""

from __future__ import annotations

from dataclasses import dataclass, field

from .panels import OverriddenPanel
from .utils import DEFAULT_WIDTH


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

    def right_of(self, other: Group) -> Group:
        """Place a new group to the right of the other object."""
        shifted_group = self
        new_x = other.right_x
        new_y = other.y
        if new_x + self.right_x > DEFAULT_WIDTH:
            new_x = 0
            new_y = other.lowest_point
        shifted_group.x = new_x
        shifted_group.y = new_y
        for i, _ in enumerate(shifted_group.panels):
            shifted_group.panels[i].x += new_x
            shifted_group.panels[i].y += new_y
        return shifted_group

    def below(self, other: Group) -> Group:
        """Place a new group below the other object."""
        shifted_group = self
        new_x = other.x
        new_y = other.lowest_point
        shifted_group.x = new_x
        shifted_group.y = new_y
        for i, _ in enumerate(shifted_group.panels):
            shifted_group.panels[i].y += new_y
        return shifted_group
