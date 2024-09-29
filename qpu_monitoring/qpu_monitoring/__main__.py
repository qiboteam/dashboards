import argparse
import datetime as dt
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).parents[1] / "scripts"
RUNCARD = Path(__file__).parents[1] / "runcards" / "monitor.yml"
REPORTS = Path.home() / "monitoring_reports"
SLURM_JOBS = Path.home() / "monitoring_jobs"


TEMPLATE_SCRIPT_NAMES = {
    "qpu_monitor_job.sh": "qpu_monitor_template.sh",
    "slurm_monitor_submit.sh": "slurm_submit_template.sh",
}
"""Names of the rendered templates."""


@dataclass
class SlurmJobInfo:
    partition: Optional[str]
    """Slurm partition on which to run monitoring.
    If set to None, run the script locally."""
    platform: Optional[str]
    """Qibolab platform on which to run the monitoring script.
    If set to None, default to dummy."""
    targets: Optional[list[str]]
    """List of targets to be monitored."""
    qibolab_platforms_path: Path
    """Path of the platforms for qibolab."""

    def __post_init__(self):
        """If platform is set to None, default to "dummy"."""
        if self.platform is None:
            self.platform = "dummy"
        if self.targets is None:
            self.targets = [0]


def generate_monitoring_script(
    job_info: SlurmJobInfo,
    monitoring_script_path: Path,
    report_save_path: Path = None,
):
    """Create bash scripts for slurm and qibocal auto with jinja.

    Args:
        job_info: object containing information on where to run the specific monitoring job.
        monitoring_script_path: the path where to save the generated bash script.
            Currently scripts are saved to
            <user_home>/monitoring_jobs/<platform_name>
        report_save_path: where to save the qibocal report.
            Currently reports are saved to
            <user_home>/monitoring_reports/<platform_name>/timestamp
            where timestamp is in the format "%Year%Month%Day_%Hours%Minutes%Seconds"
            (YYYYmmdd_HHMMSS).
    """
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template(TEMPLATE_SCRIPT_NAMES[monitoring_script_path.name])
    monitoring_script = template.render(
        slurm_partition=job_info.partition,
        platform=job_info.platform,
        targets=" ".join(job_info.targets),
        report_path=report_save_path,
        qibolab_platforms_path=job_info.qibolab_platforms_path,
        monitoring_script_path=Path(__file__).parents[1] / "scripts" / "monitoring.py",
    )
    monitoring_script_path.parent.mkdir(parents=True, exist_ok=True)
    monitoring_script_path.write_text(monitoring_script)
    monitoring_script_path.chmod(0o744)


def monitor_qpu(job_info: SlurmJobInfo):
    """Run qpu monitoring.

    If platform is set to dummy, do not use slurm and run
    qq locally instead.
    """
    current_timestamp = dt.datetime.now().strftime(r"%Y%m%d_%H%M%S")
    try:
        script_path = SLURM_JOBS / job_info.platform
        report_save_path = REPORTS / job_info.platform / current_timestamp
        generate_monitoring_script(
            job_info,
            script_path / "slurm_monitor_submit.sh",
        )
        generate_monitoring_script(
            job_info,
            script_path / "qpu_monitor_job.sh",
            report_save_path,
        )
        # run acquisition job on slurm
        if job_info.partition is None:
            subprocess.run([script_path / "qpu_monitor_job.sh"])
        else:
            # use sbatch
            subprocess.run([script_path / "slurm_monitor_submit.sh"], cwd=script_path)
    except Exception as e:
        print(e)
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slurm_configuration", type=str, nargs="?", default=None)
    parser.add_argument("--qibolab_platforms_path", type=Path, nargs="?", default=None)
    args = parser.parse_args()

    if args.slurm_configuration is None:
        job = SlurmJobInfo(None, None, None, args.qibolab_platforms_path)
    else:
        slurm_configuration = json.loads(args.slurm_configuration)
        job = SlurmJobInfo(
            **slurm_configuration, qibolab_platforms_path=args.qibolab_platforms_path
        )
    monitor_qpu(job)


if __name__ == "__main__":
    main()
