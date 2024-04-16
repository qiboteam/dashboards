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


@dataclass
class SlurmJobInfo:
    partition: str
    platform: str


def generate_slurm_script(
    job_info: SlurmJobInfo,
    slurm_script_path: Path,
    report_save_path: Path,
):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template("slurm_template.sh")
    slurm_monitoring_script = template.render(
        slurm_partition=job_info.partition,
        platform=job_info.platform,
        runcard_path=RUNCARD,
        report_path=report_save_path,
    )
    slurm_script_path.parent.mkdir(parents=True, exist_ok=True)
    slurm_script_path.write_text(slurm_monitoring_script)
    slurm_script_path.chmod(0o744)


def generate_monitoring_script(
    job_info: SlurmJobInfo,
    slurm_script_path: Path,
):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template("monitoring_template.sh")
    slurm_monitoring_script = template.render(
        slurm_partition=job_info.partition,
        platform=job_info.platform,
    )
    slurm_script_path.parent.mkdir(parents=True, exist_ok=True)
    slurm_script_path.write_text(slurm_monitoring_script)
    slurm_script_path.chmod(0o744)


def monitor_qpu(job_info: SlurmJobInfo):
    try:
        platform = job_info.platform
        if platform is None:
            platform = "dummy"
        script_path = SLURM_JOBS / platform
        report_save_path = REPORTS / platform
        # generate slurm script
        script_path = SLURM_JOBS / job_info.platform
        report_save_path = REPORTS / job_info.platform
        generate_slurm_script(job_info, script_path / "monitor.sh", report_save_path)
        generate_monitoring_script(
            job_info,
            script_path / "slurm_qpu_monitor.sh",
        )
        # run acquisition job on slurm
        if job_info.partition is None:
            subprocess.run([script_path / "monitor.sh"])
        else:
            # use sbatch
            subprocess.run([script_path / "slurm_qpu_monitor.sh"], cwd=script_path)
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
