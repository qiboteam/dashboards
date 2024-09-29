import argparse
import json
import logging
from pathlib import Path

from .metrics_export import export_metrics
from .ssh_utils import copy_back_remote_report, key_based_connect

logger = logging.getLogger(__name__)


def monitor_qpu(
    qpu_information: dict[str, str],
    hostname: str,
    username: str,
    private_key_password: str = None,
):
    """Run monitoring on the specified qpu and export results."""
    client = key_based_connect(hostname, username, private_key_password)
    _, _, sbatch_errors = client.exec_command(
        "source .qpu_monitoring_env/bin/activate;"
        "python -m qpu_monitoring --slurm_configuration "
        f"'{json.dumps([qpu_information])}' --qibolab_platforms_path $HOME/qibolab_platforms_qrc"
    )
    logger.info(sbatch_errors.readlines())
    # after sbatch finishes, copy back the results
    _, command_line_output, _ = client.exec_command(
        "cd monitoring_reports;"
        f"cd {qpu_information['platform']};"
        "OUTPUT_DIR=$(ls -t | head -1);"
        "echo $OUTPUT_DIR"
    )
    qibocal_report_folder_name = command_line_output.readlines()[0].rstrip()
    report_save_path = copy_back_remote_report(
        client,
        qpu_information["platform"],
        qibocal_report_folder_name,
        "~/monitoring_reports",
        Path.home() / "monitoring_reports",
    )
    # export results to the database
    postgres_info = {
        "username": "dash_admin",
        "password": "dash_admin",
        "container": "postgres",
        "port": 5432,
        "database": "qpu_metrics",
    }
    export_metrics(report_save_path, export_database="postgres", **postgres_info)


def main():
    """ssh connection"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--username", type=str, default="qibocal")
    parser.add_argument("--private_key_password", type=str, default=None)
    parser.add_argument("--slurm_configuration", type=str, default=None)
    args = parser.parse_args()

    # slurm_configuration = json.loads(args.slurm_configuration)
    slurm_configuration = '[{"partition":"qw11q","platform":"qw11q"}]'
    slurm_configuration = json.loads(slurm_configuration)
    for qpu in slurm_configuration:
        monitor_qpu(qpu, args.host, args.username, args.private_key_password)


if __name__ == "__main__":
    main()
