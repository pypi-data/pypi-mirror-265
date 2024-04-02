import logging
from os import getenv
from os import mkdir
from pathlib import Path
from logging.config import dictConfig

LOGS_PATH = Path(__file__).resolve().parent.parent.parent / "logs"

if not LOGS_PATH.is_dir():
    mkdir(LOGS_PATH)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "files": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_PATH / "log.log",
            "mode": "a",
            "maxBytes": 4096,
            "backupCount": 5
        },
        "ow_files": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOGS_PATH / "log.log",
            "mode": "w+",
        }
    },
    "loggers": {
        "": {
            "handlers": ["files"],
            "level": "INFO",
            "propagate": False
        },
        "debug": {
            "handlers": ["ow_files"],
            "level": "DEBUG",
            "propagate": False
        }
    }

}

dictConfig(LOGGING_CONFIG)


def get_logger_or_debug(name: str) -> logging.Logger | None:
    """
    If the CLYPHER_DEBUG environment flag is set to True, return the 
    debug logger.

    Else, return a logger instantiated with the name arg.
    """

    debug = getenv("CLYPHER_DEBUG", "False").lower() in ("true", "t", "1")

    if debug:
        return logging.getLogger("debug")
    
    else:
        return logging.getLogger(name)
    