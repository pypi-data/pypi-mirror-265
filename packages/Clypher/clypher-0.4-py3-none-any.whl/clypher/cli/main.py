import typer
from os import environ
from .commands import (
    version,
    encryption,
    decryption,
    )


app = typer.Typer(
    pretty_exceptions_enable=environ.get(
        "CLYPHER_DEBUG", "false").lower() in ("true", "1")
)

app.add_typer(version.app)
app.command(name="enc", help="Encrypt files or the contents of a directory.")(encryption.encrypt)
app.command(name="dec", help="Decrypt files or the contents of a directory.")(decryption.decrypt)