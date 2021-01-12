from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class ArcsightToRegistryKey(ValueTransformer):
    """A value transformer to convert Arcsight Registry root key to windows-registry-key STIX"""

    @staticmethod
    def transform(registry_key):
        stix_root_keys_mapping = {"HKLM": "HKEY_LOCAL_MACHINE", "HKCU": "HKEY_CURRENT_USER",
                                  "HKCR": "HKEY_CLASSES_ROOT", "HKCC": "HKEY_CURRENT_CONFIG",
                                  "HKPD": "HKEY_PERFORMANCE_DATA", "HKU": "HKEY_USERS", "HKDD": "HKEY_DYN_DATA"}
        try:
            root_key = registry_key.split("\\")
            map_root_key = stix_root_keys_mapping[root_key[0]]
            root_key[0] = map_root_key
            converted_root_key = '\\'.join(root_key)
            return converted_root_key
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")


class ArcsightToRegistryValue(ValueTransformer):
    """A value transformer to convert Arcsight Registry type to STIX format"""

    @staticmethod
    def transform(registry_values):
        stix_datatype_mapping = {"DWORD": "REG_DWORD", "EXPAND_SZ": "REG_EXPAND_SZ", "MULTI_SZ": "REG_MULTI_SZ",
                                 "BINARY": "REG_BINARY", "QWORD": "REG_QWORD", "NONE": "REG_NONE",
                                 "default_type": "REG_SZ"}
        converted_value = list()
        registry_value_dict = dict()
        for each_value in registry_values:
            for key in each_value:
                is_type = False
                if key == "registry_string":
                    for reg_type in stix_datatype_mapping.keys():
                        if reg_type in each_value[key]:
                            is_type = True
                            registry_value_dict['data_type'] = stix_datatype_mapping[reg_type]
                            registry_value_dict['data'] = each_value[key].replace(reg_type, '').strip()
                    if not is_type:
                        registry_value_dict['data_type'] = stix_datatype_mapping["default_type"]
                        registry_value_dict['data'] = each_value[key]
                if key == "name":
                    registry_value_dict[key] = each_value[key]
        converted_value.append(registry_value_dict)

        return converted_value


class ArcsightFormatMac(ValueTransformer):
    """A value transformer to convert Mac address to STIX Mac address format"""

    @staticmethod
    def transform(mac):
        value = mac.replace("-", ":")
        return value.lower()
