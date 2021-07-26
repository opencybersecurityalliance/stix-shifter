# -*- coding: utf-8 -*-
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

WINDOWS_KEY_MAPPING = {
    "HKCC": "HKEY_CURRENT_CONFIG",
    "HKCR": "HKEY_CLASSES_ROOT",
    "HKCU": "HKEY_CURRENT_USER",
    "HKDD": "HKEY_DYN_DATA",
    "HKLM": "HKEY_LOCAL_MACHINE",
    "HKPD": "HKEY_PERFORMANCE_DATA",
    "HKU": "HKEY_USERS",
}


class ConvertInternetHeaders(ValueTransformer):

    @staticmethod
    def transform(obj: list):
        return {data.get("HeaderName"): data.get("Value") for data in obj}


class ConvertWindowsRegistry(ValueTransformer):
    @staticmethod
    def transform(obj: str):
        try:
            final_result = obj
            root_key_index = obj.index("\\") if "\\" in obj else -1
            if root_key_index != -1:
                full_key = WINDOWS_KEY_MAPPING.get(obj[0:root_key_index].upper())
                if full_key:
                    final_result = full_key + obj[root_key_index:]

            return final_result
        except BaseException as e:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key due to %s", e)
        return obj
