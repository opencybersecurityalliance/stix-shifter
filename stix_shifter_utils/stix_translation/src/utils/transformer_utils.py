import inspect
import importlib.util
from stix_shifter_utils.utils.logger import set_logger


def get_module_transformers(module=None):
    module_path = None
    if module:
        module_path = f"stix_shifter_modules.{module}.stix_translation.transformers"
    return __get_transformers(module_path)

def __get_transformers(module_path):
    transformers = __load_transformers("stix_shifter_utils.stix_translation.src.utils.transformers")
    if module_path:
        transformers.update(__load_transformers(module_path))
    return transformers

def __load_transformers(path):
    transformers = {}
    try:
        for name, cls in inspect.getmembers(importlib.import_module(path), inspect.isclass):
            if cls.__module__.startswith(path):
                transformers[name] = cls
    except:
        logger = set_logger(__name__)
        logger.debug(f'no transformer found in {path}')
    return transformers
