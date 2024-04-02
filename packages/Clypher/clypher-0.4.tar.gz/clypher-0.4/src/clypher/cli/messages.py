from rich.align import Align
from .._version import __version__

VERSIONMSG = f"[bold blue]Clypher[/bold blue] v[bold cyan]{__version__}[/bold cyan]"

BANNER = Align(
    f"""[bold cyan]
   ___ _             _               
  / __\ |_   _ _ __ | |__   ___ _ __ 
 / /  | | | | | '_ \| '_ \ / _ \ '__|
/ /___| | |_| | |_) | | | |  __/ |   
\____/|_|\__, | .__/|_| |_|\___|_|   
         |___/|_| v{__version__}

[/bold cyan]""", align="center")