import re
import ntpath
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class SplunkToTimestamp(ValueTransformer):
    """A value transformer for converting Splunk timestamp to regular timestamp"""
    @staticmethod
    def transform(splunkTime):
        return splunkTime[:-6] + 'Z'


class SplunkHash(ValueTransformer):
    """
    A value transformer for converting the following hash format, into multiple fields.

    Example for Sysmon hashes:

    Input: "process_hash": "MD5=5A0B0E6F407C89916515328F318842A1,SHA256=8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91,IMPHASH=406DD24835F1447987FB607C78597252",

    Desired output:
    "hashes": {
                        "MD5": "5A0B0E6F407C89916515328F318842A1",
                        "SHA256":"8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91,
                        "IMPHASH": "406DD24835F1447987FB607C78597252"
                    }

    """

    @staticmethod
    def transform(obj):
        def get_pair_of_hash(hash_raw):
            """
            :param hash_raw: Expected input of the following form MD5=5A0B0E6F407C89916515328F318842A1
            :return:
            """
            if hash_raw:
                if "SHA1" in hash_raw:
                    hash_raw = hash_raw.replace("SHA1","SHA-1")
                elif "SHA256" in hash_raw:
                    hash_raw = hash_raw.replace("SHA256", "SHA-256")
                elif "IMPHASH" in hash_raw:
                    hash_raw = hash_raw.replace("IMPHASH", "x_IMPHASH")
                splitted = hash_raw.split("=")
                if len(splitted) != 2:
                    raise ValueError("hash should be in the format of <hash_name=hash_value>")
                return splitted[0], splitted[1]

        # expected to be string
        if obj:
            hashes = str(obj).split(",")
            if len(hashes) == 1 and '=' not in hashes[0]:
                return obj
            hashes = dict(map(lambda x: get_pair_of_hash(x), hashes))
            return hashes


class SplunkMacFormatChange(ValueTransformer):
    """    A value transformer for converting MAC value into stix format(using : separator)  """
    @staticmethod
    def transform(macvalue):
        """correcting mac address presentation, it should be 6 octate separated
         by only colon (:) not by any other special character """
        macvalue = re.sub("[^A-Fa-f0-9]", "", macvalue)
        maclength = len(macvalue)
        if (maclength < 12):
            for i in range(maclength, 12):
                macvalue = "0" + macvalue

        value = ':'.join([macvalue[i:i + 2] for i in range(0, len(macvalue), 2)])
        return value.lower()


class ConvertHexAndStringToInteger(ValueTransformer):
    """ converts hexadecimal and string values to integer """
    @staticmethod
    def transform(pidvalue):
        if isinstance(pidvalue, int):
            return pidvalue
        else:
            if pidvalue.startswith('0x'):
                return int(pidvalue, 16)
            else:
                return int(pidvalue)


class SeverityToScore(ValueTransformer):
    """value transformer to convert severity string value to integer value on a scale of 1-100"""
    @staticmethod
    def transform(severity):
        severity_string_to_integer = {"informational": 20,
                                      "low": 40,
                                      "medium": 60,
                                      "high": 80,
                                      "critical": 100
                                      }
        try:
            return severity_string_to_integer[severity]

        except KeyError:
            LOGGER.error("Cannot convert string to severity scale value")


class CheckProcessName(ValueTransformer):
    """ Check process name, if it contains path then remove it."""
    @staticmethod
    def transform(value):
        try:
            _, file_name = ntpath.split(value)
            return file_name
        except ValueError:
            LOGGER.error("Cannot convert input to file name string")


class CheckProcessPath(ValueTransformer):
    """ Check process path, if it contains filename then remove it."""
    @staticmethod
    def transform(value):
        try:
            file_path, _ = ntpath.split(value)
            return file_path
        except ValueError:
            LOGGER.error("Cannot convert input to file path string")


class RegistryValueName(ValueTransformer):
    """changing Hive into expanded form"""
    @staticmethod
    def transform(registry):        
        reghive_dict = {'HKLM':'HKEY_LOCAL_MACHINE', 'hklm': 'hkey_local_machine',
                        'HKCU': 'HKEY_CURRENT_USER', 'hkcu': 'hkey_current_user',
                        'HKCR': 'HKEY_CLASSES_ROOT', 'hkcr': 'hkey_classes_root',
                        'HKU': 'HKEY_USERS', 'hku': 'hkey_users',
                        'HKCC': 'HKEY_CURRENT_CONFIG', 'hkcc': 'hkey_current_config',
                        'HKPD': 'HKEY_PERFORMANCE_DATA', 'hkpd': 'hkey_performance_data'}

        registry = str(registry)
        data = registry.split('\\')
        expand_key = reghive_dict.get(data[0])
        if expand_key is not None:
            replaced_key = registry.replace(data[0], expand_key)
            return replaced_key
        return registry
            

class FormatToStixRegistryValue(ValueTransformer):
    """A value transformer to convert Registry value to windows-registry-key.value STIX"""

    @staticmethod
    def transform(obj):

        try:
            stix_mapping = {"registryValueName": "name", "registryValueData": "data"}
            converted_value = []
            #for each_value in obj:
            registryvalue_dict = {}
            for key, value in obj.items():
                registryvalue_dict.update({stix_mapping[key]: value})
            converted_value.append(registryvalue_dict)
            return converted_value

        except ValueError:
            LOGGER.error("Cannot convert root value to Stix formatted windows registry value")            

class FormatTimestamp(ValueTransformer):
    """A value transformer for converting timestamp to regular timestamp"""
    @staticmethod
    def transform(splunkTime):
        try:
            if splunkTime[10] == " " and len(splunkTime) > 10:
                splunkTime = splunkTime.replace(" ", "T")
            if splunkTime[-1] != "Z" or splunkTime[-1] != "z":
                splunkTime = splunkTime + "Z"
        except ValueError:
            LOGGER.error("Error while converting timestamp") 
        return splunkTime
