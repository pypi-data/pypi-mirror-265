import importlib
from ..engines import INSTALLED_ENGINES
import os 

from ..logging_config.logger_config import get_logger_or_debug

LOG = get_logger_or_debug(__name__)

def import_engine(engine:str, engine_list: dict = INSTALLED_ENGINES):
    """
    Given a string engine, return the engine class that it represents.

    :param engine: The command-line name of the engine, specified by the user.
    :type engine: str
    :param engine_list: A dictionary containing the list of installed engines, defaults to INSTALLED_ENGINES.
    :type engine_list: dict, optional
    :raise AttributeError: If the specified engine module exists, but the Engine class doesn't.
    :raise ImportError: If the engine cannot be imported.
    :raise KeyError: If the specified engine module doesn't exist.
    """
    print(os.getcwd())

    try:
        engine = engine_list[engine]
        LOG.debug(f"Trying to import engine '{engine}'.")
        module_name, class_name = engine.rsplit(".", 1)

        LOG.debug(f"Module name: {module_name}, class name: {class_name}")
        module = importlib.import_module(module_name)
        engine_class = getattr(module, class_name)

        return engine_class

    except AttributeError as e:
        LOG.exception(f"Engine import raised {e}.")
        raise e(f"The specified engine module {module_name} has no class {class_name}.")

    except ImportError as e:
        LOG.exception(f"Engine import raised {e}.")

        raise e
        raise SystemExit(f"The engine {engine} does not exist. Are you sure it is installed?")
    
    except KeyError as e:
        LOG.exception(f"Engine import raised {e}.")
    
        raise SystemExit(f"The specified engine {engine} does not exist in the INSTALLED_ENGINES list.")

