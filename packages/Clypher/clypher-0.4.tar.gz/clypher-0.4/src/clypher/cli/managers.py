from .messages import *
from .._console import console, stderr_console
from rich.progress import (
    Progress,
    )

import typer

class ConsoleManager:
    """
    The class responsible for pretty printing in the console.
    """

    @staticmethod
    def print_version_msg():
        """
        Print the current version message.
        """
        console.print(VERSIONMSG)

    @staticmethod
    def print_banner():
        """
        Print the Clypher banner.
        """
        console.print(BANNER)

    @staticmethod
    def error(msg: str, show_tag: bool = True, color_msg: bool = True, newline: bool = False):
        """
        Display a bold [ERROR] tag in red, followed by the message in msg, also in red.
    
        :param msg: The message to print.
        :type msg: str
        :param show_tag: Show or hide the [ERROR] tag, defaults to True.
        :type show_tag: bool, optional.
        :param color_msg: Also display the message in red, defaults to True.
        :type color_msg: bool, optional.
        :param newline: Append a newline before the message, defaults to False.
        :type newline: bool, optional.

        """
        if newline:
            message = "\n"
        else:
            message = ""

        if show_tag:
            message += "[bold red]\[ERROR]: [/bold red]"

        if color_msg:
            message += f"[red]{msg}[/red]"
        else:
            message += msg

        stderr_console.print(message)

    @staticmethod
    def warn(msg: str, show_tag: bool = True, color_msg: bool = True):
        """
        Display a bold [WARNING] tag in red, followed by the message in msg, also in red.

        :param msg: The message to print.
        :type msg: str
        :param show_tag: Show the [WARNING] tag. If False, hide it, defaults to True.
        :type show_tag: bool, optional.
        :param color_msg: Also display the message in red, defaults to True.
        :type color_msg: bool, optional.
        """

        message = ""

        if show_tag:
            message += "[bold red]\[WARNING]: [/bold red]"

        if color_msg:
            message += f"[red]{msg}[/red]"
        else:
            message += msg

        console.print(message)

    @staticmethod
    def info(msg: str, show_tag: bool = True):
        """
        Display a bold [INFO] tag in blue, followed by msg.

        :param msg: The message to print.
        :type msg: str
        :param show_tag: Show the [INFO] tag. If False, hide it, defaults to True.
        :type show_tag: bool, optional.
        """

        message = ""

        if show_tag:
            message += "[bold bright_blue]\[INFO]: [/bold bright_blue]"

        message += msg

        console.print(message)

    @staticmethod
    def success(msg: str, show_tag: bool = True):
        """
        Display a bold [SUCCESS] tag in green, followed by msg.

        :param msg: The message to print.
        :type msg: str
        :param show_tag: Show the [SUCCESS] tag. If False, hide it, defaults to True.
        :type show_tag: bool, optional.
        """

        message = ""

        if show_tag:
            message += "[bold bright_green]\[SUCCESS]: [/bold bright_green]"

        message += msg

        console.print(message)

    @staticmethod
    def ask_password(mode: str = "encryption") -> str:
        """
        Prompt the user for a password, depending on `mode`.

        :param mode: The mode in which the program is working.
            This changes the displayed message, defaults to 'encryption'.
        :type mode: str, optional
        :returns: The password as plaintext.
        :rtype str:
        """

        if mode == "encryption":
            ConsoleManager.warn("Choose a password carefully.")
            console.print(
                "Once encrypted, [bold red] the file CANNOT be restored unless the correct password is provided.[/bold red]")

            return typer.prompt(
                text="Enter a password to be used for the file encryption",
                hide_input=True,
                confirmation_prompt=True)
        
        elif mode == "decryption":
            return typer.prompt(
                text="Enter the file password",
                hide_input=True,
                )
        
        else:
            raise ValueError(f"The mode '{mode}' is not recognized as a valid mode for prompting a password.")

    @staticmethod
    def prompt(msg: str, *args, **kwargs) -> str:
        """
        Prompt the user. args and kwargs are passed to typer.prompt()

        :param msg: The message to show the user.
        :type msg: str
        :returns: Whatever the user wrote.
        :rtype str:
        """
        return typer.prompt(text=msg, *args, **kwargs)
    
    @staticmethod
    def confirm(msg: str, *args, **kwargs) -> bool:
        """
        Prompt the user for confirmation. args and kwargs are passed to typer.prompt()

        :param msg: The message to show the user.
        :type msg: str
        :returns: Whatever the user selected.
        :rtype bool:
        """
        return typer.confirm(text=msg, *args, **kwargs)

class ProgressManager:
    """
    Thin wrapper around Rich's Progress class. Provides a single method to interact with it.

    :param msg: The message to show next to the progress bar.
    :type msg: str
    :param total: The number of steps
    :type total: int
    """

    def __init__(self, msg: str, total: int) -> None:
        #: The progress instance, used as a context manager.
        self.progress = Progress()
        #: The current task.
        self._task = self.progress.add_task(msg, total=total)

    def step(self, msg: str | None = None) -> None:
        """
        Update the current task.

        :param msg: If it isn't None, update the progress bar description.
        :type msg: str, optional
        """

        if msg is not None:
            self.progress.print(msg)

        self.progress.update(self._task, advance=1)

    def stop(self):
        return self.progress.stop()