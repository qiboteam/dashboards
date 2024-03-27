from pathlib import Path

GRAFANA_PORT = "3000"
"""Port of grafana defined in compose.yaml"""
GRAFANA_CONTAINER_NAME = "grafana"
"""Name of the grafana container defined in compose.yaml"""

ADMIN_USERNAME = "admin"
"""Default name of the admin user."""
ADMIN_PASSWORD = "admin"
"""Default password of the admin user."""

GRAFANA_URL = f"http://{GRAFANA_CONTAINER_NAME}:{GRAFANA_PORT}/api"
"""Url of the api for the grafana container without authentication."""
GRAFANA_URL_AUTHENTICATED = f"http://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@{GRAFANA_CONTAINER_NAME}:{GRAFANA_PORT}/api"
"""Url of the api for the grafana container with basic user authentication."""

TEMPLATES_PATH = Path(__file__).parent / "templates"
"""Path of the directory containing json templates used for grafana."""

DATASOURCE_CONFIGURATION_PATH = Path(__file__).parent / "config" / "datasources.json"
