#!/usr/bin/env python3
from datetime import datetime, timezone, tzinfo, timedelta
import base64
import socket
import re
import os
import ntpath

from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

class ValueTransformer():
    """ Base class for value transformers """

    @staticmethod
    def transform(obj):
        """ abstract function for converting value formats """
        raise NotImplementedError


class StringToBool(ValueTransformer):
    """A value transformer for converting String to boolean value"""

    @staticmethod
    def transform(value):
        return value.lower() in ("yes", "true", "t", "1")


class SplunkToTimestamp(ValueTransformer):
    """A value transformer for converting Splunk timestamp to regular timestamp"""

    @staticmethod
    def transform(splunkTime):
        return splunkTime[:-6]+'Z'


class EpochToTimestamp(ValueTransformer):
    """A value transformer for the timestamps"""

    @staticmethod
    def transform(epoch):
        try:
            return (datetime.fromtimestamp(int(epoch) / 1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        except ValueError:
            LOGGER.error("Cannot convert epoch value {} to timestamp".format(epoch))


class FormatMac(ValueTransformer):
    """A value transformer to convert Mac address to STIX Mac address format"""

    @staticmethod
    def transform(mac):
        value = ':'.join([mac[i:i + 2] for i in range(0, len(mac), 2)])
        return value.lower()


class MsatpToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds"""

    @staticmethod
    def transform(msatptime):
        time_array = msatptime.split('.')
        converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
        return converted_time


class FormatTCPProtocol(ValueTransformer):
    """A value transformer to convert TCP protocol to IANA format"""

    @staticmethod
    def transform(protocolname):
        converted_name = re.search(r'^tcp', protocolname, re.I).group(0)
        try:
            obj_array = converted_name if isinstance(converted_name, list) else converted_name.split(', ')
            # Loop through entries inside obj_array and make all strings lowercase to meet STIX format
            obj_array = [entry.lower() for entry in obj_array]
            return obj_array
        except ValueError:
            LOGGER.error("Cannot convert input to array")


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


class AwsToTimestamp(ValueTransformer):
    """
    A value transformer for converting AWS timestamp (YYYY-MM-DD hh:mm:ss.000)
    to UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z)
    """

    @staticmethod
    def transform(aws_time):
        time_array = aws_time.split(' ')
        converted_time = time_array[0] + 'T' + time_array[1] + 'Z'
        return converted_time


class EpochSecondsToTimestamp(ValueTransformer):
    """A value transformer for the timestamps"""

    @staticmethod
    def transform(epoch):
        try:
            return (datetime.fromtimestamp(int(epoch), timezone.utc)
                    .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        except ValueError:
            LOGGER.error("Cannot convert epoch value {} to timestamp".format(epoch))


class TimestampToMilliseconds(ValueTransformer):
    """
    A value transformer for converting a UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z) 
    to 13-digit Unix time (epoch + milliseconds)
    """

    @staticmethod
    def transform(timestamp):
        time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
        epoch = datetime(1970, 1, 1)
        try:
            converted_time = int(((datetime.strptime(timestamp, time_pattern) - epoch).total_seconds()) * 1000)
            return converted_time
        except ValueError:
            LOGGER.error("Cannot convert the timestamp {} to milliseconds".format(timestamp))


class ToInteger(ValueTransformer):
    """A value transformer for expected integer values"""

    @staticmethod
    def transform(obj):
        try:
            if type(obj) is str and re.search('\.', obj):
                obj = float(obj)
            return int(obj)
        except ValueError:
            LOGGER.error("Cannot convert input {} to integer".format(obj))


class ToString(ValueTransformer):
    """A value transformer for expected string values"""

    @staticmethod
    def transform(obj):
        try:
            return str(obj)
        except ValueError:
            LOGGER.error("Cannot convert input to string")


class ToLowercaseArray(ValueTransformer):
    """A value transformer for expected array values"""

    @staticmethod
    def transform(obj):
        try:
            obj_array = obj if isinstance(obj, list) else obj.split(', ')
            # Loop through entries inside obj_array and make all strings lowercase to meet STIX format
            obj_array = [entry.lower() for entry in obj_array]
            return obj_array
        except ValueError:
            LOGGER.error("Cannot convert input to array")


class ToBase64(ValueTransformer):
    """A value transformer for expected base 64 values"""

    @staticmethod
    def transform(obj):
        try:
            return base64.b64encode(obj.encode('ascii')).decode('ascii')
        except ValueError:
            LOGGER.error("Cannot convert input to base64")


class ToFilePath(ValueTransformer):
    """A value transformer for expected file paths"""

    @staticmethod
    def transform(obj):
        try:
            return obj[0:len(obj) - len(re.split(r'[\\/]', obj)[-1])]
        except ValueError:
            LOGGER.error("Cannot convert input to path string")


class ToDirectoryPath(ValueTransformer):
    """A value transformer for expected directory path"""

    @staticmethod
    def transform(obj):
        try:
            file_path, file_name = ntpath.split(obj)
            return file_path
        except ValueError:
            LOGGER.error("Cannot convert input to directory path string")


class ToFileName(ValueTransformer):
    """A value transformer for expected file names"""

    @staticmethod
    def transform(obj):
        try:
            return re.split(r'[\\/]', obj)[-1]
        except ValueError:
            LOGGER.error("Cannot convert input to file name")


class ToDomainName(ValueTransformer):
    """A value transformer for expected domain name"""

    @staticmethod
    def transform(url):
        try:
            if url is None:
                return
            splits = url.split("://")
            i = (0,1)[len(splits)>1]
            domain_name = splits[i].split("?")[0].split('/')[0].split(':')[0].lower()
            return domain_name
        except ValueError:
            LOGGER.error("Cannot convert input to domain name")


class ToIPv4(ValueTransformer):
    """A value transformer for converting an unsigned long to IPv4 string"""

    @staticmethod
    def transform(value):
        try:
            return socket.inet_ntoa((value & 0xffffffff).to_bytes(4, "big"))
        except ValueError:
            LOGGER.error("Cannot convert input to IPv4 string")


class DateTimeToUnixTimestamp(ValueTransformer):
    """A value transformer for converting python datetime object to Unix (millisecond) timestamp"""

    @staticmethod
    def transform(obj):
        try:
            return int((obj - datetime(1970, 1, 1)).total_seconds() * 1000)
        except ValueError:
            LOGGER.error("Cannot convert input {} to Unix timestamp".format(obj))


class NaiveToUTC(tzinfo):
    """
        A class for converting naive datetime object to UTC timezone datetime object
        naive datetime: "2017-09-29T15:00:00
        datetime with timezone offset: "2017-09-29T15:00:00+0300
        This class is declared to help convert Naive datetime format to datetime format with timezone(UTC here)
        """
    _dst = timedelta(0)

    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return self.__class__._dst

    def dst(self, dt):
        return self.__class__._dst


class TimestampToUTC(ValueTransformer):
    """
    A value transformer for converting a UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z)
    to %d %b %Y %H:%M:%S %z"(23 Oct 2018 12:20:14 +0000)
    """

    @staticmethod
    def transform(timestamp, is_default=False):
        """
        Transformer for converting naive or non-naive to UTC time
        :param timestamp: datetime.datetime object(datetime.datetime(2019, 8, 22, 15, 44, 11, 716805)) or
                            '2019-07-25T10:43:10.003Z'
        :param is_default: True if timestamp like '2019-07-25T10:43:10.003Z'
                            False if timestamp like datetime.datetime(2019, 8, 22, 15, 44, 11, 716805)
        :return: str, e.g. : 25 Jul 2019 10:43:10 +0000
        """
        if re.search(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(timestamp)):
            input_time_pattern = '%Y-%m-%dT%H:%M:%SZ'
        else:
            input_time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
        output_time_pattern = '%d %b %Y %H:%M:%S %z'
        if not is_default:
            # convert timestamp to datetime object
            datetime_obj = datetime.strptime(timestamp, input_time_pattern)
        else:
            datetime_obj = timestamp
        converted_time = datetime.strftime(datetime_obj.replace(tzinfo=NaiveToUTC()), output_time_pattern)
        return converted_time


class SetToOne(ValueTransformer):
    """Send back integer = 1 irrespective of the obj"""

    @staticmethod
    def transform(obj):
        try:
            return int("1")
        except ValueError:
            LOGGER.error("Cannot convert input {} to integer".format(obj))

# TODO: rename classes to be more generic since they can be reused by other data sources


class EpochToGuardium(ValueTransformer):
    """A value transformer for Epoch to Guardium timestamp"""

    @staticmethod
    def transform(epoch):
        try:
            return (datetime.fromtimestamp(int(epoch) / 1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
        except ValueError:
            LOGGER.error("Cannot convert epoch value {} to timestamp".format(epoch))


class GuardiumToTimestamp(ValueTransformer):
    """A value transformer for converting Guardium timestamp to regular timestamp"""

    @staticmethod
    def transform(gdmTime):
        rgx = r"(\d\d\d\d-\d\d-\d\d)\s(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, gdmTime))[0]
        return (mtch[0] + 'T' + mtch[1]) + '.000Z'


class TimestampToGuardium(ValueTransformer):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(timestamp):
        rgx = r"(\d\d\d\d-\d\d-\d\d).(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, timestamp))[0]
        return (mtch[0] + ' ' + mtch[1])


class GuardiumQS(ValueTransformer):
    """Send back Policy Violation string"""

    @staticmethod
    def transform(obj):
        return "Policy Violation"


class GuardiumRep(ValueTransformer):
    """Send back Threat Case string"""

    @staticmethod
    def transform(obj):
        return "Threat Case"


class GuardiumMapSeverity(object):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(severity):
        try:
            num = int(severity)
            if num < 5:
                return "Low"
            elif num > 5:
                return "High"
            else:
                return "Medium"
        except ValueError:
            LOGGER.error("Cannot convert input to path string")


class GuardiumMapSeverityNum(object):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(severity):
        sev = severity.lower()
        if sev == "low":
            return '1'
        elif sev == "high":
            return '9'
        elif sev == "medium":
            return '5'
        else:
            return "*"


class TimestampToGuardiumQS(ValueTransformer):
    """A value transformer for converting  regular timestamp to Guardium timestamp"""

    @staticmethod
    def transform(timestamp):
        rgx = r"(\d\d\d\d-\d\d-\d\d).(\d\d:\d\d:\d\d)"
        mtch = (re.findall(rgx, timestamp))[0]
        return mtch[0].replace("-", "") + ' ' + mtch[1]


class Ymd_HMSToTimestamp(ValueTransformer):
    """A value transformer for the timestamps but adds ONE second to the time stamp.  Reason: Use when modified date is missing"""

    @staticmethod
    def transform(dt_Str):
        dt_obj = datetime.strptime(dt_Str, '%Y-%m-%d %H:%M:%S')
        dt_objOne = dt_obj + timedelta(seconds=1)
        return (datetime.fromtimestamp(datetime.timestamp(dt_objOne), timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')


def get_all_transformers():
    return {"SplunkToTimestamp": SplunkToTimestamp, "EpochToTimestamp": EpochToTimestamp, "ToInteger": ToInteger, "ToString": ToString,
            "ToLowercaseArray": ToLowercaseArray, "ToBase64": ToBase64, "ToFilePath": ToFilePath, "ToFileName": ToFileName,
            "StringToBool": StringToBool, "ToDomainName": ToDomainName, "TimestampToMilliseconds": TimestampToMilliseconds,
            "EpochSecondsToTimestamp": EpochSecondsToTimestamp, "ToIPv4": ToIPv4,
            "DateTimeToUnixTimestamp": DateTimeToUnixTimestamp, "NaiveTimestampToUTC": TimestampToUTC,
            "ToDirectoryPath": ToDirectoryPath, "MsatpToTimestamp": MsatpToTimestamp, "FormatTCPProtocol": FormatTCPProtocol,
            "MsatpToRegistryValue": MsatpToRegistryValue, "FormatMac": FormatMac,
            "SetToOne": SetToOne, "Ymd_HMSToTimestamp": Ymd_HMSToTimestamp, "TimestampToGuardium": TimestampToGuardium,
            "TimestampToGuardiumQS": TimestampToGuardiumQS, "GuardiumToTimestamp": GuardiumToTimestamp,
            "EpochToGuardium": EpochToGuardium, "AwsToTimestamp": AwsToTimestamp, "GuardiumRep": GuardiumRep,
            "GuardiumQS": GuardiumQS, "GuardiumMapSeverity": GuardiumMapSeverity,
            "GuardiumMapSeverityNum": GuardiumMapSeverityNum}
