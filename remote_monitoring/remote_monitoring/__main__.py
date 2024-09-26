import argparse
import json
import logging
from pathlib import Path

from .utils import copy_back_remote_report, key_based_connect

logger = logging.getLogger(__name__)


def main():
    """ssh connection"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--username", type=str, default="qibocal")
    parser.add_argument("--private_key_password", type=str, default=None)
    parser.add_argument("--slurm_configuration", type=str, default=None)
    args = parser.parse_args()
    client = key_based_connect(
        args.host, args.username, private_key_password=args.private_key_password
    )

    slurm_configuration = json.loads(args.slurm_configuration)
    _, _, sbatch_errors = client.exec_command(
        "source .qpu_monitoring_env/bin/activate;"
        "python -m qpu_monitoring --slurm_configuration "
        f"'{json.dumps(slurm_configuration)}' --qibolab_platforms_path $HOME/qibolab_platforms_qrc"
    )
    logger.info(sbatch_errors.readlines())

    for qpu in slurm_configuration:
        _, command_line_output, _ = client.exec_command(
            "cd monitoring_reports;"
            f"cd {qpu['platform']};"
            "OUTPUT_DIR=$(ls -t | head -1);"
            "echo $OUTPUT_DIR"
        )
        qibocal_report_folder_name = command_line_output.readlines()[0].rstrip()
        copy_back_remote_report(
            client,
            qpu["platform"],
            qibocal_report_folder_name,
            "~/monitoring_reports",
            Path.home() / "monitoring_reports",
        )


if __name__ == "__main__":
    main()
