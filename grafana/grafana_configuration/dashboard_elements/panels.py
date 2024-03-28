from typing import Optional

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
        self.overrides = [target.override() for target in self.targets]
        panel_dictionary = super().to_json_data()
        if self.grid_pos is None:
            raise ValueError("Panel grid position must be set.")
        panel_dictionary["gridPos"] = self.grid_pos.__dict__
        return panel_dictionary


class Stat(glc.Stat):
    """Wrapper class of `grafanalib.core.Stat`."""

    def __init__(self, *args, unit: str = "", grid_pos: GridPos = None, **kwargs):
        super().__init__(*args, format=unit, **kwargs)
        self.grid_pos = grid_pos

    def to_json_data(self):
        """Wrapper of `grafanalib.core.TimeSeries.to_json_data`."""
        self.overrides = [target.override() for target in self.targets]
        panel_dictionary = super().to_json_data()
        if self.grid_pos is None:
            raise ValueError("Panel grid position must be set.")
        panel_dictionary["gridPos"] = self.grid_pos.__dict__
        return panel_dictionary
