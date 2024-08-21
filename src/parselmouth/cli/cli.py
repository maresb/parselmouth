from typing import Annotated
import typer


from parselmouth.internals.updater_producer import main as updater_producer_main
from parselmouth.internals.updater import main as updater_main
from parselmouth.internals.update_one import main as update_one_main
from parselmouth.internals.updater_merger import main as update_merger_main

app = typer.Typer()


@app.callback()
def main():
    """
    \bParselmouth is a tool used to generate a conda < -- > pypi mapping.
     It's functionality can be split up in three main parts:
    - `Updater producer` - this is the part that generates the subdir@letter list.
    - `Updater` - it's main responsibility is to use the subdir@letter list to generate the mapping.
    - `Updater merger` - it merges the partial mappings into a single mapping file which is later uploaded.
    """
    pass


@app.command()
def updater_producer(output_dir: str = "output_index", check_if_exists: bool = True):
    """
    Generate the subdir@letter list.
    """

    updater_producer_main(output_dir=output_dir, check_if_exists=check_if_exists)


@app.command()
def updater(
    subdir_letter: Annotated[
        str,
        typer.Argument(
            help="Pass subdir@letter to get the new packages. Example: passing `noarch@s` will get all the packages from noarch subdir which start with `s` letter."
        ),
    ],
    output_dir: str = "output_index",
    partial_output_dir: str = "output",
    upload: bool = False,
):
    """
    Get all the packages based on subdir@letter and save it in partial_output_dir.
    To save requests to S3, we save our index in output_dir after running `updater-producer` command.

    Use `--upload` to enable uploading to S3. ( This is used in CI )

    """

    updater_main(
        subdir_letter=subdir_letter,
        output_dir=output_dir,
        partial_output_dir=partial_output_dir,
        upload=upload,
    )


@app.command()
def updater_merger(output_dir: str = "output"):
    """
    This is used to merge all the partial mappings into a single mapping file during the CI run.

    """

    update_merger_main(output_dir)


@app.command()
def update_one(
    package_name: Annotated[
        str,
        typer.Argument(
            help="Pass full package name to get the mapping for it. Example: `warp-lang-1.3.0-cpu38_h19ae9ab_0.conda.`"
        ),
    ],
    subdir: Annotated[
        str,
        typer.Argument(help="Subdir for the package name"),
    ],
    backend: Annotated[
        str,
        typer.Option(
            help="What backend to use for the package. Supported backends: oci, libcfgraph, streamed."
        ),
    ],
    upload: Annotated[
        bool,
        typer.Option(help="Upload or overwrite already existing mapping."),
    ],
):
    """
    Check mapping just for one package.
    """

    update_one_main(
        package_name=package_name, subdir=subdir, backend_type=backend, upload=upload
    )