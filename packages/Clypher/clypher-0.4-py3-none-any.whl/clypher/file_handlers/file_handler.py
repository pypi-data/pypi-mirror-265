from os.path import (
    exists,
)

from pathlib import Path
from .._version import __version__
from ..logging_config.logger_config import get_logger_or_debug
from ..file_handlers.base_filehandler import BaseFileHandler
from ..cli.managers import ConsoleManager as CONSOLE


LOG = get_logger_or_debug(__name__)


class FileHandler(BaseFileHandler):
    """
    Deals with file reading and writing, as well as with handling IOErrors and creating
    containers.
    """

    def __init__(
        self,
        files: list[Path],
        output_dir: Path | None = None,
        force_overwrite: bool = False,
        decrypting: bool = False,
        recursive: bool = False,
    ) -> None:

        super().__init__(files, output_dir, force_overwrite, recursive=recursive)

        LOG.debug(f"FileHandler file list: {self.file_list}")

        self.decrypting = decrypting
        self.file_list = self._generate_file_list(self.file_list)
        self.file_ammount = len(self.file_list)
        self.recursive = recursive


    def is_empty(self) -> bool:
        """
        If no more files are available, return True.
        
        :returns: True if there are no more files available. False otherwise
        :rtype bool:
        """

        return self.file_ammount == 0

    def _generate_output_path(self, currfile: Path) -> Path:
        """
        Given a file path, generate and return its corresponding output file name.
        """

        # if --out is specified, then take that as the base output path
        # Otherwise, take the parent dir of each file.
        if self.out is not None:
            base_output_path = self.out
        else:
            base_output_path = currfile.parent

        if self.decrypting:
            outfile = base_output_path / Path(currfile.name.rstrip(".clypher"))

        else:
            outfile = base_output_path / Path(currfile.name + ".clypher")

        return outfile

    def _generate_file_list(self, infiles: list[Path]) -> list[tuple[Path, Path]]:
        """
        Given a list of input file paths, generate and return a list of tuples of the form
        (input_filename, output_filename).
        """
        file_list = []

        for file_ in infiles:

            # Ignore all files that do not end with .clypher when decrypting
            if self.decrypting and not file_.name.endswith(".clypher"):
                continue
            #TODO: If the user specified a file without a .clypher extension, then it should probably
            # not be ignored.
            # This would mean somehow distinguishing between auto discovery of files or explicitly 
            # entering a file name

            output_path = self._generate_output_path(file_)

            if exists(output_path) and self.force_ow is False:
                CONSOLE.error(
                    f"The output file for ({output_path}) for the input file ({file_}) already exists."
                )
                raise FileExistsError(
                    f"The output file for ({output_path}) for the input file ({file_}) already exists."
                )

            file_list.append((file_, output_path))

        LOG.debug(f"Generated file list: {file_list}")
        return file_list

    def request(self) -> bytes | None:
        """
        Reads and returns the next file to be processed as bytes, along with its filename,
        or None if there are no more files to process.
        """
        try:
            self.currfile, self.output_filepath = self.file_list.pop()
            self.file_ammount = len(self.file_list)
            
            LOG.debug(f"Requested file: {self.currfile}")

            with open(self.currfile, "rb") as f:

                return f.read()

        except IndexError:
            return None

    def write(self, data: bytes) -> int:
        """
        Write data to the file and return the number of bytes written.
        """
        LOG.debug(f"Writing file {self.output_filepath}...")
        with open(self.output_filepath, "wb") as f:
            return f.write(data)
