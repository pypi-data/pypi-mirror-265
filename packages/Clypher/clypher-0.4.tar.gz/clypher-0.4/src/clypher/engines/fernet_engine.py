from ..encryptors.fernet_encryptor import FernetEncryptor
from ..logging_config.logger_config import get_logger_or_debug
from ..file_handlers.file_handler import FileHandler
from ..cli.managers import ConsoleManager as CONSOLE
from ..cli.managers import ProgressManager as PM
from .base_engine import BaseEngine

from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken

LOG = get_logger_or_debug(__name__)


class FernetEngine(BaseEngine):
    def __init__(self, decrypting: bool = False, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.__encryptor = FernetEncryptor(
            password=self.plaintext_password,
        )

        self.__fhandler = FileHandler(
            files=self.infiles,
            output_dir=self.output,
            force_overwrite=self.force_ow,
            decrypting=decrypting,
            recursive=kwargs.get("recursive", False)
        )

    def _recursion_confirmation(self) -> bool:
        """
        Display the list of files to be processed if the program is running in recursive mode.
        After that, display a confirmation prompt to the user. Return the answer.
        """

        if self.__fhandler.recursive:
            CONSOLE.warn(
                f"Recursive mode is on, take a look at the list of files to be processed:")

            for file_, _ in self.__fhandler.file_list:
                CONSOLE.info(str(file_), show_tag=False)

            return CONSOLE.confirm("Do you want to proceed with the operation? ")
        
        else: return True

    def start_encryption(self):

        if not self._recursion_confirmation():
            LOG.info(f"User aborted encryption after reading recursive file list.")
            CONSOLE.info(f"Aborting..")
            return

        CONSOLE.info(
            f"Starting encryption. {self.__fhandler.file_ammount} files to encrypt.\n")
        LOG.info(
            f"Starting encryption... {self.__fhandler.file_ammount} files to encrypt.")
        files_processed = 0
        files_skipped = 0

        progress_manager = PM("[cyan]Encrypting...[/cyan]", self.__fhandler.file_ammount)
        try:
            with progress_manager.progress:

                file_ = self.__fhandler.request()

                while file_ is not None:

                    if len(file_) == 0:
                        progress_manager.step(
                            f"{self.__fhandler.currfile} is empty. Skipping...")

                        files_skipped += 1

                        LOG.info(
                            f"{self.__fhandler.currfile} is empty. Skipping...")

                    else:
                        progress_manager.step(self.__fhandler.currfile)

                        LOG.info(
                            f"Encrypting file {self.__fhandler.currfile}...")

                        self.__fhandler.write(
                            self.__encryptor.encrypt(
                                file_
                            )
                        )

                        files_processed += 1

                        LOG.info(f"Done")

                    file_ = self.__fhandler.request()

        except KeyboardInterrupt:
            CONSOLE.warn(
                f"Stopped encryption after {files_processed + files_skipped} files.\n")

        if files_processed > 0 or files_skipped > 0:
            CONSOLE.success(
                f"Successfully encrypted {files_processed} files. {files_skipped} skipped.\n")

    def start_decryption(self):

        if not self._recursion_confirmation():
            LOG.info(f"User aborted decryption after reading recursive file list.")
            CONSOLE.info(f"Aborting..")
            return

        if self.__fhandler.is_empty():
            CONSOLE.info(
                f"No encrypted files found. Are you sure they have a .clypher extension?")
            return

        CONSOLE.info(
            f"Starting decryption. {self.__fhandler.file_ammount} files to decrypt.\n")
        files_processed = 0
        files_skipped = 0

        progress_manager = PM("[cyan]Dencrypting...[/cyan]", self.__fhandler.file_ammount)
        try:
            with progress_manager.progress:

                file_ = self.__fhandler.request()

                while file_ is not None:

                    if len(file_) == 0:
                        progress_manager.step(
                            f"{self.__fhandler.currfile} is empty. Skipping...")

                        files_skipped += 1

                        LOG.info(
                            f"{self.__fhandler.currfile} is empty. Skipping...")

                    else:
                        progress_manager.step(self.__fhandler.currfile)

                        LOG.info(
                            f"Decrypting file {self.__fhandler.currfile}...")

                        self.__fhandler.write(
                            self.__encryptor.decrypt(
                                file_
                            )
                        )

                        files_processed += 1

                        LOG.info(f"Done")

                    file_ = self.__fhandler.request()

        except KeyboardInterrupt:
            CONSOLE.warn(
                f"Stopped decryption after {files_processed + files_skipped} files.")

        except (InvalidSignature, InvalidToken):
            progress_manager.stop()
            CONSOLE.error(
                (
                    "The specified file doesn't appear to have been encrypted with the Fernet engine,"
                    " or the specified password is incorrect."
                )
            )

        if files_processed > 0:
            CONSOLE.success(f"Successfully decrypted {files_processed} files.")
