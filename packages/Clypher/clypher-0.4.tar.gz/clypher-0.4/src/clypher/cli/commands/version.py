import typer
from ...cli.managers import ConsoleManager as CONSOLE
app = typer.Typer()

@app.callback(invoke_without_command=True, help="Print the current package version.")
def version():
    CONSOLE.print_version_msg()
