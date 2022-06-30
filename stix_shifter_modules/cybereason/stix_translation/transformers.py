from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class PathToStixRegistryKey(ValueTransformer):
    """A value transformer to convert Cybereason Registry path to windows-registry-key.key STIX"""

    @staticmethod
    def transform(registry):

        stix_root_keys_mapping = {"hklm": "HKEY_LOCAL_MACHINE", "hkcu": "HKEY_CURRENT_USER",
                                  "hkcr": "HKEY_CLASSES_ROOT", "hkcc": "HKEY_CURRENT_CONFIG",
                                  "hkpd": "HKEY_PERFORMANCE_DATA", "hku": "HKEY_USERS", "hkdd": "HKEY_DYN_DATA"}
        try:
            splited = registry.split("\\")
            if splited[0] in stix_root_keys_mapping:
                map_root_key = stix_root_keys_mapping[splited[0]]
                splited[0] = map_root_key
            key = '\\'.join(splited)
            return key
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")
        return None
