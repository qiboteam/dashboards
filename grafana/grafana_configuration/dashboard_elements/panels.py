from typing import Union

import grafanalib.core as glc


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
        **kwargs
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

    @property
    def y(self):
        return self.gridPos["y"]

    @property
    def right_x(self):
        return self.x + self.gridPos["w"]

    @property
    def lowest_point(self) -> int:
        return self.y + self.gridPos["h"]

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
        **kwargs
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

    @property
    def y(self):
        return self.gridPos["y"]

    @property
    def right_x(self):
        return self.x + self.gridPos["w"]

    @property
    def lowest_point(self) -> int:
        return self.y + self.gridPos["h"]

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
