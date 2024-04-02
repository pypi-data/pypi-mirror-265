"""
Clypher. Encrypt files from the command line.
Copyright (C) 2024 Maximiliano Cancelarich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

For contacting me, send me an email at maximilianoacan@gmail.com.

Please be aware that this program IS NOT INTENDED as a cryptographically secure encryption solution.
"""

import sys
import logging

from os import environ

from .cli.managers import ConsoleManager as CONSOLE
from .cli.main import app

debug = environ.get("CLYPHER_DEBUG", False)

if debug is False:
    sys.tracebacklimit = 0
    LOG = logging.getLogger(__name__)

else:
    sys.tracebacklimit = -1
    LOG = logging.getLogger("debug")


def main():
    CONSOLE.print_banner()
    app()


if __name__ == "__main__":

    main()
