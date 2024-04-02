from abc import ABC, abstractmethod
from pathlib import Path
from os.path import (
    abspath,
    join,

)
from os import (
    listdir,
    walk
)
from pathlib import Path


class BaseFileHandler(ABC):
    """
    Provides a simple base interface for new file handlers.
    Resolves all input paths and converts them into absolute paths.

    Can also recursively walk a directory, adding all its files to the input.

    Is also able to resolve relative input paths such as " **.** " and "**../foo**".

    :param files: The list of input paths coming from the CLI.
    :type files: list[Path]
    :param output_dir: The output directory, defaults to the current working dir.
    :type output_dir: Path or None, optional
    :param force_overwrite: Force overwriting output files, defaults to True.
    :type force_overwrite: bool, optional
    :param recursive: Recursively walk all input directories,
        adding all files to the input, default to False.
    :type recursive: bool, optional
    :raises FileNotFoundError: If any input path, or the output directory, doesn't exist.
    :raises ValueError: If the output directory is a file.
    """

    def __init__(
        self,
        files: list[Path],
        output_dir: Path | None = None,
        force_overwrite: bool = False,
        recursive: bool = False
    ) -> None:

        # Make all input paths absolute, and walk any directories listing all files.
        processed_paths = set()

        for path in files:

            path = Path(abspath(path))

            if path.is_file():
                processed_paths.add(path)

            elif path.is_dir():
                for file_ in self.list_files(path, recursive=recursive):
                    processed_paths.add(file_)

            else:
                raise FileNotFoundError(f"The path {path} doesn't exist.")

        #: The list of input files. Every entry is an absolute path.
        self.file_list = processed_paths

        if output_dir is not None:
            output_dir = Path(abspath(output_dir))

            if output_dir.is_file():
                raise ValueError(
                    f"The output must be a directory, not a file.")

            elif output_dir.is_dir():
                pass

            else:
                raise FileNotFoundError(
                    f"The output path {output_dir} doesn't exist.")

        #: Output directory.
        self.out = output_dir

        #: Force overwriting of output files.
        self.force_ow = force_overwrite

    def list_files(self, path: Path, recursive: bool = False) -> list[Path]:
        """
        List all the files in the current directory and return a list of absolute paths.
        If recursive, recursively walk the directory, listing all files.

        :param path: The path to list all files from.
        :type path: Path
        :param recursive: If True, recursively walk the directory, adding all files to the input.
            (default is False)
        :type recursive: bool, optional
        :return: A list of absolute paths.
        :rtype: list[Path]
        """
        entries = set()

        if recursive:
            for dirname, _, filenames in walk(path):
                for file_ in filenames:
                    entry = Path(join(dirname, file_))

                    entries.add(
                        Path(join(path, entry))
                    )
        else:
            for entry in listdir(path):
                entry = Path(join(path, entry))

                if entry.is_file():

                    entries.add(entry)

        return entries

    @abstractmethod
    def request():
        """
        Return the next file to process. Must be implemented by a concrete class.
        """
        raise NotImplementedError(f"Classes inheriting from BaseFileHandler must implement a request() method.")

    @abstractmethod
    def write():
        """
        Given bytes, write them to a file. Must be implemented by a concrete class.
        """
        raise NotImplementedError("Classes inheriting from a BaseFileHandler must implement a write() method.")


if __name__ == "__main__":
    fh = BaseFileHandler(["clypher/"], recursive=True)
    print(fh.file_list)
