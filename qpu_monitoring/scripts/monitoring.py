import argparse
from pathlib import Path
from typing import Union

from qibo.backends import construct_backend
from qibocal.auto.execute import Executor
from qibocal.auto.history import History
from qibocal.auto.output import Metadata, Output
from qibocal.auto.task import Completed
from qibocal.cli.report import report
from qibolab.platform import Platform
from qibolab.qubits import QubitId

MAX_CHI2 = 5
"""Maximum chi2 to allow platform update."""


def target_type(value: str) -> Union[int, str]:
    """Cast the target id to `int` if possible, otherwise keep it as a string."""
    try:
        return int(value)
    except ValueError:
        return value


def check_chi2(
    node: Completed,
    platform: Platform,
    targets: list[QubitId],
    max_chi2: float = MAX_CHI2,
):
    """Chi2 control and update."""
    for target in targets:
        try:
            getattr(node.results[target], "chi2")
            try:
                node.results.chi2[target]

                if node.results.chi2[target][0] > max_chi2:
                    print(
                        f"{node.task.id} has chi2 {node.results.chi2[target][0]} greater than {max_chi2}. Stopping."
                    )
                else:
                    node.update_platform(platform)
            except KeyError:
                pass
        except AttributeError:
            node.update_platform(platform)


def main(targets: list, platform_name: str, output_folder: str):
    with Executor.open(
        "myexec",
        path=output_folder,
        platform=platform_name,
        targets=targets,
        update=False,
        force=True,
    ) as e:

        t1_output = e.t1(
            delay_before_readout_start=10,
            delay_before_readout_end=100000,
            delay_before_readout_step=500,
            nshots=1024,
        )

        check_chi2(t1_output, platform=e.platform, targets=targets)

        ramsey_output = e.ramsey(
            delay_between_pulses_start=10,
            delay_between_pulses_end=100000,
            delay_between_pulses_step=500,
            nshots=1024,
        )

        check_chi2(ramsey_output, platform=e.platform, targets=targets)


        ro_char_output = e.readout_characterization(nshots=5000, delay=1000)

        check_chi2(ro_char_output, platform=e.platform, targets=targets)

        report(e.path, e.history)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Qubit recalibration")
    parser.add_argument("--platform", type=str, help="Qibo platform")
    parser.add_argument(
        "--output", default="monitoring", type=Path, help="Output folder"
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        type=target_type,
        help="Target qubit to recalibrate",
        required=True,
    )

    args = parser.parse_args()
    main(targets=args.targets, platform_name=args.platform, output_folder=args.output)
