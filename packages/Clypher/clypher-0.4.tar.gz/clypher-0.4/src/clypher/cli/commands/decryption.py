import typer

from typing import List, Optional
from pathlib import Path
from typing_extensions import Annotated

from ...cli.managers import ConsoleManager as CONSOLE
from ...import_handler.import_handler import import_engine



def decrypt(
    input_files: Annotated[
        List[Path],
        typer.Argument()
    ] = None,
    out: Annotated[
        Optional[Path],
        typer.Option(help="Output directory name.")
    ] = None,
    password: Annotated[
        Optional[str],
        typer.Option(
            "--pass",
            help="Pass the password as an option.")
    ] = None,
    force_overwrite: Annotated[
        bool,
        typer.Option(
            "--fo",
            help="If used, force the app to overwrite any output files that may already exist. Defaults to False."
        )
    ] = False,
    engine: Annotated[
        Optional[str],
        typer.Option(help="The encryption engine to use.")
    ] = "fernet",

    recursive: Annotated[
        Optional[bool],
        typer.Option(
            "--recursive",
            help="If used, recursively traverse any input directories, adding each file as an input. Use with caution."
        )
    ] = False
):
    
    if not input_files:
        CONSOLE.error("No input was provided.")
        raise SystemExit(1)

    if password is None:
        password = CONSOLE.ask_password(mode="decryption")

    engine_class = import_engine(engine)

    engine_instance = engine_class(
        password=password,
        infiles=input_files,
        output=out,
        force_ow=force_overwrite,
        decrypting = True,
        recursive = recursive
    )

    engine_instance.start_decryption()