import grafanalib.core as glc


class Override:
    def __init__(
        self, name: str = "", color: str = None, thresholds: list[list] = None
    ):
        """Initialize object.

        Args:
            name (str): label of the variable in the Panel to be overridden.
            color (str): color of the line of the variable.
            thresholds (list[list]): list of colors and relative thresholds
                colors are string, thresholds are numbers (the first one in None), e.g.:
                [["first_color", None], ["second_color", lower_threshold]]
        """
        self.name = name
        self.color = color
        self.thresholds = thresholds

    def to_json_data(self):
        properties = []
        if self.color is not None:
            override_color = {
                "id": "color",
                "value": {
                    "mode": "fixed",
                    "fixedColor": self.color,
                },
            }
            properties.append(override_color)
        if self.thresholds is not None:
            color_steps = [
                {"color": threshold[0], "value": threshold[1]}
                for threshold in self.thresholds
            ]
            override_color = {
                "id": "thresholds",
                "value": {
                    "mode": "absolute",
                    "steps": color_steps,
                },
            }
            properties.append(override_color)
        return {
            "matcher": {
                "id": "byName",
                "options": self.name,
            },
            "properties": properties,
        }


class Target(glc.Target):
    def __init__(
        self, *args, color: str = None, thresholds: list[list] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.color = color
        self.thresholds = thresholds

    def override(self):
        return Override(self.legendFormat, color=self.color, thresholds=self.thresholds)
