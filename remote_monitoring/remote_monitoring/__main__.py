import argparse
import json
import logging

logger = logging.getLogger(__name__)

from .monitoring import monitor_qpu


def main():
    """ssh connection"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--username", type=str, default="qibocal")
    parser.add_argument("--private_key_password", type=str, default=None)
    parser.add_argument("--slurm_configuration", type=str, default=None)
    args = parser.parse_args()

    slurm_configuration = json.loads(args.slurm_configuration)
    for qpu in slurm_configuration:
        monitor_qpu(qpu, args.host, args.username, args.private_key_password)


if __name__ == "__main__":
    main()
