import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .metrics_export import export_metrics

TEMPLATES = Path(__file__).parents[1] / "scripts"
RUNCARD = Path(__file__).parents[1] / "runcards" / "monitor.yml"
REPORTS = Path.home() / "monitoring_reports"
SLURM_JOBS = Path.home() / "monitoring_jobs"


def generate_slurm_script(
    slurm_partition: str,
    qibolab_platform: str,
    slurm_script_path: Path,
    report_save_path: Path,
):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template("slurm_template.sh")
    slurm_monitoring_script = template.render(
        slurm_partition=slurm_partition,
        platform=qibolab_platform,
        runcard_path=RUNCARD,
        report_path=report_save_path,
    )
    slurm_script_path.parent.mkdir(parents=True, exist_ok=True)
    slurm_script_path.write_text(slurm_monitoring_script)
    slurm_script_path.chmod(0o744)


def generate_monitoring_script(
    slurm_partition: str,
    qibolab_platform: str,
    slurm_script_path: Path,
):
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    template = env.get_template("monitoring_template.sh")
    slurm_monitoring_script = template.render(
        slurm_partition=slurm_partition,
        platform=qibolab_platform,
    )
    slurm_script_path.parent.mkdir(parents=True, exist_ok=True)
    slurm_script_path.write_text(slurm_monitoring_script)
    slurm_script_path.chmod(0o744)


def monitor_qpu(slurm_partition: str = None, qibolab_platform: str = "dummy"):
    # generate slurm script
    script_path = SLURM_JOBS / qibolab_platform
    report_save_path = REPORTS / qibolab_platform
    generate_slurm_script(
        slurm_partition, qibolab_platform, script_path / "monitor.sh", report_save_path
    )
    generate_monitoring_script(
        slurm_partition,
        qibolab_platform,
        script_path / "slurm_qpu_monitor.sh",
    )
    # run acquisition job on slurm
    if slurm_partition is None:
        subprocess.run([script_path / "monitor.sh"])
    else:
        # use sbatch
        subprocess.run([script_path / "slurm_qpu_monitor.sh"], cwd=script_path)
    # process acquired data
    export_metrics(report_save_path)


def main():
    jobs = [
        ("slurm_partition", "qibolab_platform"),
    ]
    for job in jobs:
        monitor_qpu(*job)


if __name__ == "__main__":
    main()
