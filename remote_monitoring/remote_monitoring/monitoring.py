import json
import logging
from pathlib import Path

from paramiko import SSHClient

from .metrics_export import export_metrics
from .ssh_utils import copy_back_remote_report, key_based_connect

logger = logging.getLogger(__name__)


def acquire(
    ssh_client: SSHClient, qpu_information: dict[str, str], qibolab_platforms_path: Path
):
    """Acquire metrics from the remote cluster."""
    _, sbatch_output, sbatch_errors = ssh_client.exec_command(
        "module load qibo;"
        "python -m qpu_monitoring --slurm_configuration "
        f"'{json.dumps(qpu_information)}' --qibolab_platforms_path {qibolab_platforms_path}"
    )
    logger.info(sbatch_output.readlines())
    error_message = sbatch_errors.readlines()
    if len(error_message) > 0:
        logger.error(error_message)
        message = "".join(error_message)
        if "sbatch: error: invalid partition specified:" in message:
            raise ValueError(message)
        if "Another job is currently running for " in message:
            raise Exception(message)
        if f"Platform {qpu_information['platform']} not found." in message:
            raise ValueError(message)
        if "Traceback (most recent call last):" in message:
            # Error in the python code submitted to slurm (or run locally)
            raise Exception(message)


def retrieve_results(ssh_client: SSHClient, qpu_information: dict[str, str]) -> Path:
    """after sbatch finishes, copy back the results."""
    _, command_line_output, _ = ssh_client.exec_command(
        "cd monitoring_reports;"
        f"cd {qpu_information['platform']};"
        "OUTPUT_DIR=$(ls -t | head -1);"
        "echo $OUTPUT_DIR"
    )
    qibocal_report_folder_name = command_line_output.readlines()[0].rstrip()
    return copy_back_remote_report(
        ssh_client,
        qpu_information["platform"],
        qibocal_report_folder_name,
        "~/monitoring_reports",
        Path.home() / "monitoring_reports",
    )


def sql_export(report_save_path: Path):
    # export results to the database
    postgres_info = {
        "username": "dash_admin",
        "password": "dash_admin",
        "container": "postgres",
        "port": 5432,
        "database": "qpu_metrics",
    }
    export_metrics(report_save_path, export_database="postgres", **postgres_info)


def monitor_qpu(
    qpu_information: dict[str, str],
    hostname: str,
    username: str,
    qibolab_platforms_path: Path,
    private_key_password: str = None,
):
    """Run monitoring on the specified qpu and export results."""
    client = key_based_connect(hostname, username, private_key_password)
    acquire(client, qpu_information, qibolab_platforms_path)
    report_save_path = retrieve_results(client, qpu_information)
    sql_export(report_save_path)
