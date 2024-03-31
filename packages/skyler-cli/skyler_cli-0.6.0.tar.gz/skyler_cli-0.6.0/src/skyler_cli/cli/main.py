from enum import Enum
from pathlib import Path
import rich
import pydicom
import typer

from ..core.bootstrap.system import SystemBootstrapper, OS, MachineType

help_msg = "Skyler CLI: The multitool I always wanted to build myself"
app = typer.Typer(
    help=help_msg,
    no_args_is_help=True,
)


@app.command()
def setup_configs(
    os: OS = typer.Option(..., prompt="Select your OS"),
    machine_type: MachineType = typer.Option(
        ..., prompt="What type of machine is this?"
    ),
    personal_machine: bool = typer.Option(
        ..., prompt="Is this a personal machine (as opposed to one for work)"
    ),
    dryrun: bool = typer.Option(False, is_flag=True),
):
    bootstrapper = SystemBootstrapper(os, machine_type, is_personal=personal_machine)
    if dryrun:
        print(
            f"Dryrun! Would have set up the system with: {os=} {machine_type=} {personal_machine=}"
        )
        return

    bootstrapper.bootstrap_system()


class OutputFormat(Enum):
    PPRINT = "pprint"
    JSON = "json"


@app.command(help="Parse a single dicom file, and pretty print the file metadata")
def dicom(
    in_file: Path,
    fmt: OutputFormat = typer.Option(default="pprint"),
):
    dicom_data = pydicom.dcmread(in_file)
    if fmt == OutputFormat.PPRINT:
        rich.print(repr(dicom_data))
    elif fmt == OutputFormat.JSON:
        rich.print_json(
            dicom_data.to_json(
                bulk_data_threshold=100,
                bulk_data_element_handler=lambda bulk_data: None,
            )
        )
    else:
        print(f"Unsupported output format: {fmt}")


if __name__ == "__main__":
    app()
