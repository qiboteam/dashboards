import argparse
import json
import subprocess
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .metrics_export import export_metrics

TEMPLATES = Path(__file__).parents[1] / "scripts"
RUNCARD = Path(__file__).parents[1] / "runcards" / "monitor.yml"
REPORTS = Path.home() / "monitoring_reports"
SLURM_JOBS = Path.home() / "monitoring_jobs"


TEMPLATE_SCRIPT_NAMES = {
    "qpu_monitor_job.sh": "qpu_monitor_template.sh",
    "slurm_monitor_submit.sh": "slurm_submit_template.sh",
}


@dataclass
class SlurmJobInfo:
    partition: str
    platform: str

    def __post_init__(self):
        """If platform is set to None, default to "dummy"."""
        if self.platform is None:
            self.platform = "dummy"


def generate_monitoring_script(
    job_info: SlurmJobInfo,
    monitoring_script_path: Path,
    report_save_path: Path = None,
):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template(TEMPLATE_SCRIPT_NAMES[monitoring_script_path.name])
    monitoring_script = template.render(
        slurm_partition=job_info.partition,
        platform=job_info.platform,
        runcard_path=RUNCARD,
        report_path=report_save_path,
    )
    monitoring_script_path.parent.mkdir(parents=True, exist_ok=True)
    monitoring_script_path.write_text(monitoring_script)
    monitoring_script_path.chmod(0o744)


def monitor_qpu(job_info: SlurmJobInfo):
    try:
        script_path = SLURM_JOBS / job_info.platform
        report_save_path = REPORTS / job_info.platform
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
        # process acquired data
        export_metrics(report_save_path)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slurm_configuration", type=str, nargs="?", default=None)
    args = parser.parse_args()
    if args.slurm_configuration is None:
        jobs = [SlurmJobInfo(None, None)]
    else:
        slurm_configuration = json.loads(args.slurm_configuration)
        jobs = [SlurmJobInfo(**job_info) for job_info in slurm_configuration]

    with ThreadPool(len(jobs)) as p:
        p.map(monitor_qpu, jobs)


if __name__ == "__main__":
    main()
