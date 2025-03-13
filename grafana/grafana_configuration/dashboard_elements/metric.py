"""Metrics and their SQL queries used in Grafana panels."""

from dataclasses import dataclass

from grafana_configuration.dashboard_elements.targets import Target


@dataclass
class Metric:
    """Query for the metric used in Grafana panels."""

    name: str
    color: str
    qpu_name: str
    qubit_id: str

    def to_target(self) -> Target:
        """Create a valid Target object for the metric."""
        return Target(
            color=f"{self.color}",
            datasource="postgres",
            rawSql=f"SELECT {self.name}, acquisition_time FROM qubit WHERE qpu_name='{self.qpu_name}' AND qubit_id='{self.qubit_id}'",
            sql={
                "columns": [
                    {
                        "type": "function",
                        "parameters": [
                            {
                                "type": "functionParameter",
                                "name": f"{self.name}",
                            }
                        ],
                    },
                    {
                        "type": "function",
                        "parameters": [
                            {
                                "type": "functionParameter",
                                "name": "acquisition_time",
                            },
                        ],
                    },
                ],
                "groupBy": [
                    {
                        "type": "groupBy",
                        "property": {
                            "type": "string",
                        },
                    },
                ],
                "limit": 50,
            },
            table="qubit",
            legendFormat=self.name,
        )
