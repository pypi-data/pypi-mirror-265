from abc import ABC, abstractmethod
from pathlib import Path


class BaseEngine(ABC):
    """
    A base engine class. Used as a mediator between an Encryptor class and a FileHandler class.

    :param password: The plaintext password provided by the user.
    :type password: str
    :param infiles: The list of input files.
    :type infiles: list[Path]
    :param output: The output directory.
    :type output: Path
    :param force_ow: Force overwriting of output files if they already exist.
    :type force_ow: bool 
    """

    def __init__(
        self,
        password: str,
        infiles: list[Path],
        output: Path,
        force_ow: bool,
        *args,
        **kwargs
    ) -> None:

        #: The plaintext password provided by the user
        self.plaintext_password = password
        #: The list of input files.
        self.infiles = infiles
        #: The output directory.
        self.output = output
        #: Force overwriting of output files.
        self.force_ow = force_ow

    @abstractmethod
    def start_encryption():
        """
        Start the encryption of all files. Must be implemented by a concrete Engine class.
        """
        raise NotImplementedError(f"Classes subclassing BaseEngine must define a start_encryption method.")

    @abstractmethod
    def start_decryption():
        """Start the decryption of all files. Must be implemented by a concrete Engine class."""
        raise NotImplementedError(f"Classes subclassing BaseEngine must define a start_decryption method.")
