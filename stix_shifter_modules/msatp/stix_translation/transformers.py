import json
import ntpath
import re
import urllib
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer

HIGH_SEVERITY = 99
MEDIUM_SEVERITY = 66
LOW_SEVERITY = 33
KILL_CHAIN_NAME = 'mitre-attack'

LOGGER = logger.set_logger(__name__)


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


class FormatMacList(ValueTransformer):
    """A value transformer to convert Mac address to STIX Mac address format"""

    @staticmethod
    def transform(mac_lst):
        addresses = []
        for mac in mac_lst:
            mac = mac.replace("-", "").replace(":", "")
            val = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)]).lower()
            addresses.append(val)
        return addresses


class IfValidUrl(ValueTransformer):
    """returns a url if its valid, empty string otherwise"""

    @staticmethod
    def transform(value):
        parsed_url = urllib.parse.urlparse(value)
        if parsed_url.scheme != "":
            return value
        else:
            return ""


class GetDomainName(ValueTransformer):
    """A value transformer to extract domain name from url"""

    @staticmethod
    def is_valid_domain_name(value):
        """test if value is a vaild domain name"""
        try:
            return (not re.search(r"\s", value)) and (re.compile(
                r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9][A-Za-z0-9-_]{0,61}[A-Za-z]$"
            ).match(value.encode("idna").decode("ascii")) is not None)
        except UnicodeError:
            return False

    @staticmethod
    def transform(value):
        # if it is already a domain name return it
        if GetDomainName.is_valid_domain_name(value):
            return value
        # it might be a url, parse the domain from the url
        parsed_url = urllib.parse.urlparse(value)
        return parsed_url.netloc


class ToFileName(ValueTransformer):

    @staticmethod
    def transform(value):
        try:
            _, file_name = ntpath.split(value)
            return file_name
        except ValueError:
            LOGGER.error("Cannot convert input to file name string")


class ToDirectory(ValueTransformer):

    @staticmethod
    def transform(value):
        try:
            file_path, _ = ntpath.split(value)
            return file_path
        except ValueError:
            LOGGER.error("Cannot convert input to file path string")


class ToMSATPDirectoryPath(ValueTransformer):
    """A value transformer for expected directory path. Take care of the inconsistency, sometimes shows up as a
    folder path and somtimes as a file name """

    @staticmethod
    def transform(value):
        try:
            file_path, file_name = ntpath.split(value)
            if '.' not in file_name:
                file_path = value
            return file_path
        except ValueError:
            LOGGER.error("Cannot convert input to directory path string")


class SeverityToNumericVal(ValueTransformer):
    """A value transformer to convert MSATP Severity value (high/medium/low) to numeric value"""

    @staticmethod
    def transform(severity):
        severity = severity.lower()
        if severity == 'high':
            return HIGH_SEVERITY
        elif severity == 'medium':
            return MEDIUM_SEVERITY
        else:
            return LOW_SEVERITY


class Alert(ValueTransformer):
    """A value transformer to convert MSATP Severity value (high/medium/low) to numeric value"""

    @staticmethod
    def transform(val):
        return "alert"


class JsonToString(ValueTransformer):
    """A value transformer to convert a string representing a json object to key: value string"""

    @staticmethod
    def transform(val):
        try:
            data = json.loads(val)
        except json.JSONDecodeError:
            return val
        pairs = []
        for key, value in data.items():
            pairs.append(f"{key}: {value}")
        return ", ".join(pairs)
