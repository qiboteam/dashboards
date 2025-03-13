from __future__ import annotations

from typing import Union

import grafanalib.core as glc

from .utils import DEFAULT_WIDTH


def move_right_of(dashboard_element: OverriddenPanel, other: OverriddenPanel):
    new_x = other.right_x
    new_y = other.y
    if new_x + dashboard_element.right_x > DEFAULT_WIDTH:
        new_x = 0
        new_y = other.lowest_point
    dashboard_element.x = new_x
    dashboard_element.y = new_y
    return dashboard_element


def move_below(dashboard_element: OverriddenPanel, other: OverriddenPanel):
    dashboard_element.x = other.x
    dashboard_element.y = other.lowest_point
    return dashboard_element


class TimeSeries(glc.TimeSeries):
    """Wrapper class of `grafanalib.core.TimeSeries`."""

    def __init__(
        self,
        *args,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        lineInterpolation: str = "smooth",
        **kwargs,
    ):
        super().__init__(*args, lineInterpolation=lineInterpolation, **kwargs)
        self.gridPos = {
            "x": x,
            "y": y,
            "w": width,
            "h": height,
        }

    @property
    def x(self):
        return self.gridPos["x"]

    @x.setter
    def x(self, value: int):
        self.gridPos["x"] = value

    @property
    def y(self):
        return self.gridPos["y"]

    @y.setter
    def y(self, value: int):
        self.gridPos["y"] = value

    @property
    def right_x(self) -> int:
        return self.x + self.gridPos["w"]

    @property
    def lowest_point(self) -> int:
        return self.y + self.gridPos["h"]

    def below(self, other: OverriddenPanel) -> TimeSeries:
        return move_below(self, other)

    def right_of(self, other: OverriddenPanel) -> TimeSeries:
        return move_right_of(self, other)

    def to_json_data(self):
        """Wrapper of `grafanalib.core.TimeSeries.to_json_data`."""
        return build_panel(self)


class Stat(glc.Stat):
    """Wrapper class of `grafanalib.core.Stat`."""

    def __init__(
        self,
        *args,
        x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0,
        unit: str = "",
        colorMode: str = "background",
        reduceCalc: str = "last",
        **kwargs,
    ):
        """Initialize object.

        Args:
            colorMode (str): supported values are
                - "background": color background (with gradient)
                - "value" (default for grafanalib): color only numbers and units
                - "background_solid": color background (without gradient)
                - "none": no color
            reduceCalc (str): supported values are
                - "last": display the last value of the time series (including nan).
                - "lastNotNull": display the last not null value of the time series.
                - "mean" (default for grafanalib): display the mean of the values.
                - "stdDev": display the standard deviation of the values.
        """
        super().__init__(
            *args, format=unit, colorMode=colorMode, reduceCalc=reduceCalc, **kwargs
        )
        self.gridPos = {
            "x": x,
            "y": y,
            "w": width,
            "h": height,
        }

    @property
    def x(self):
        return self.gridPos["x"]

    @x.setter
    def x(self, value: int):
        self.gridPos["x"] = value

    @property
    def y(self):
        return self.gridPos["y"]

    @y.setter
    def y(self, value: int):
        self.gridPos["y"] = value

    @property
    def right_x(self) -> int:
        return self.x + self.gridPos["w"]

    @property
    def lowest_point(self) -> int:
        return self.y + self.gridPos["h"]

    def below(self, other: OverriddenPanel) -> Stat:
        return move_below(self, other)

    def right_of(self, other: OverriddenPanel) -> Stat:
        return move_right_of(self, other)

    def to_json_data(self):
        """Wrapper of `grafanalib.core.TimeSeries.to_json_data`."""
        return build_panel(self)


OverriddenPanel = Union[Stat, TimeSeries]


def build_panel(panel: OverriddenPanel):
    """Build panel json and override targets."""
    # set customized colors and styles in the panel
    panel.overrides = [target.override() for target in panel.targets]
    panel_dictionary = super(type(panel), panel).to_json_data()
    return panel_dictionary
