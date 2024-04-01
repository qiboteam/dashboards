from typing import Optional, Union

import grafanalib.core as glc

from .utils import GridPos


class TimeSeries(glc.TimeSeries):
    """Wrapper class of `grafanalib.core.TimeSeries`."""

    grid_pos: Optional[GridPos]
    """Position of the panel. Must be set before generating the json dictionary."""

    def __init__(
        self,
        *args,
        lineInterpolation: str = "smooth",
        grid_pos: GridPos = None,
        **kwargs
    ):
        super().__init__(*args, lineInterpolation=lineInterpolation, **kwargs)
        self.grid_pos = grid_pos

    def to_json_data(self):
        """Wrapper of `grafanalib.core.TimeSeries.to_json_data`."""
        return set_panel_position(self)


class Stat(glc.Stat):
    """Wrapper class of `grafanalib.core.Stat`."""

    def __init__(
        self,
        *args,
        unit: str = "",
        grid_pos: GridPos = None,
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
        self.grid_pos = grid_pos

    def to_json_data(self):
        """Wrapper of `grafanalib.core.TimeSeries.to_json_data`."""
        return set_panel_position(self)


OverriddenPanel = Union[Stat, TimeSeries]


def set_panel_position(panel: OverriddenPanel):
    """Add panel grid position to the json dictionary of the panel.

    Panel position must be set, otherwise grafana throws a generic error.
    If the panel position is not set, raise an error.
    """
    # set customized colors and styles in the panel
    panel.overrides = [target.override() for target in panel.targets]

    panel_dictionary = super(type(panel), panel).to_json_data()
    if panel.grid_pos is None:
        raise ValueError("Panel grid position must be set.")
    panel_dictionary["gridPos"] = panel.grid_pos.__dict__
    return panel_dictionary
