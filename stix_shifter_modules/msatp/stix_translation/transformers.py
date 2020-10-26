from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

from datetime import datetime, timezone, tzinfo, timedelta
import base64
import socket
import re
import os
import ntpath
import urllib.parse

HIGH_SEVERITY = 99
MEDIUM_SEVERITY = 66
LOW_SEVERITY = 33
KILL_CHAIN_NAME = 'mitre-attack'

LOGGER = logger.set_logger(__name__)

class FormatMacList(ValueTransformer):
    """A value transformer to convert Mac address to STIX Mac address format"""

    def transform(mac_lst):
        addresses = []
        for mac in mac_lst:
            val = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)]).lower()
            addresses.append(val)
        return addresses


class GetHostNameFromDomain(ValueTransformer):
    """A value transformer to convert domain name to hostname"""

    def transform(domain_name):
        return domain_name.split('.')[0]


class GetDomainName(ValueTransformer):
    """A value transformer to extract domain name from url"""

    @staticmethod
    def transform(value):
        parsed_url = urllib.parse.urlparse(value)
        return parsed_url.netloc


class ToKillChainPhasesList(ValueTransformer):
    """A value transformer to convert category name to a list of kill-chain-phase objects"""

    @staticmethod
    def transform(value):
        dct = {'kill_chain_name': KILL_CHAIN_NAME, 'phase_name': value}
        return [dct]

class SeverityToNumericVal(ValueTransformer):
    """A value transformer to convert MSATP Severity value (high/medium/low) to numeric value"""

    @staticmethod
    def transform(severity):
        if severity == 'high':
            return HIGH_SEVERITY
        elif severity == 'medium':
            return MEDIUM_SEVERITY
        else:
            return LOW_SEVERITY

class MsatpToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds"""
    @staticmethod
    def transform(msatptime):
        time_array = msatptime.split('.')
        converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
        return converted_time


class MsatpToRegistryValue(ValueTransformer):
    """A value transformer to convert MSATP Registry value protocol to windows-registry-value-type STIX"""
    @staticmethod
    def transform(registryvalues):
        stix_mapping = {"RegistryValueName": "name", "RegistryValueData": "data", "RegistryValueType": "data_type"}
        stix_datatype_mapping = {"None": "REG_NONE", "String": "REG_SZ", "Dword": "REG_DWORD",
                                 "ExpandString": "REG_EXPAND_SZ", "MultiString": "REG_MULTI_SZ",
                                 "Binary": "REG_BINARY", "Qword": "REG_QWORD"}
        converted_value = list()
        registryvalue_dict = dict()
        for each_value in registryvalues:
            for key, value in each_value.items():
                is_data_add = True
                if key == "RegistryValueType":
                    if value in stix_datatype_mapping.keys():
                        value = stix_datatype_mapping[value]
                    else:
                        is_data_add = False
                if is_data_add:
                    registryvalue_dict.update({stix_mapping[key]: value})
        converted_value.append(registryvalue_dict)
        return converted_value
