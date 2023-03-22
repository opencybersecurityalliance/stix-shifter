from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
from datetime import datetime, timezone

LOGGER = logger.set_logger(__name__)

class ObjectnameToStixRegistryKey(ValueTransformer):
    """A value transformer to convert QRadar ObjectName to windows-registry-key.key STIX"""

    @staticmethod
    def transform(registry):

        stix_root_keys_mapping = {"HKLM": "HKEY_LOCAL_MACHINE", "HKCU": "HKEY_CURRENT_USER",
                                  "HKCR": "HKEY_CLASSES_ROOT", "HKCC": "HKEY_CURRENT_CONFIG",
                                  "HKPD": "HKEY_PERFORMANCE_DATA", "HKU": "HKEY_USERS", "HKDD": "HKEY_DYN_DATA"}
        try:
            splited = registry.split("\\")
            if splited[0] in stix_root_keys_mapping:
                map_root_key = stix_root_keys_mapping[splited[0]]
                splited[0] = map_root_key
            splited = splited[:-1]
            key = '\\'.join(splited)
            return key;
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")


class RegValueNameToStixRegistryValues(ValueTransformer):
    """A value transformer to convert elastic ecs Registry path to windows-registry-key.value STIX"""

    @staticmethod
    def transform(value):

        try:
            return [{ 'name': value }]
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")

class QRadarEpochToTimestamp(ValueTransformer):
    """A value transformer for the 13-digit timestamps, uses float(epoch) to handle exponential notation"""

    @staticmethod
    def transform(epoch):
        try:
            return (datetime.fromtimestamp(float(epoch) / 1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        except ValueError:
            LOGGER.error("Cannot convert epoch value {} to timestamp".format(epoch))
