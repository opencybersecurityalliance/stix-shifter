from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re
from datetime import datetime
LOGGER = logger.set_logger(__name__)


class HexToInteger(ValueTransformer):
    """Transform hexadecimal string to integer"""
    @staticmethod
    def transform(obj):
        try:
            if obj and isinstance(obj, str):
                if obj.isdigit():
                    obj = int(obj)  # string to integer
                else:
                    obj = int(obj, 16)  # hexa to integer
        except ValueError:
            LOGGER.error('Cannot convert input %s to integer', obj)
        return obj


class RealToNumber(ValueTransformer):
    """Transform number 0-1 into 0-100"""
    @staticmethod
    def transform(obj):
        try:
            if obj in ("None", "nan", "NaN"):
                obj = 0
            else:
                obj = float(obj)*100
        except ValueError:
            LOGGER.error('Cannot convert input %s to RealNumber', obj)
        return obj


class ConvertToReal(ValueTransformer):
    """Transform any value other than float into 0.0"""
    @staticmethod
    def transform(obj):
        try:
            if not isinstance(obj, float):
                obj = 0.0
        except ValueError:
            LOGGER.error('Cannot convert input %s to 0.0 float value', obj)
        return obj


class ConvertToFindingType(ValueTransformer):
    """Transform data source value to corresponding finding value"""
    @staticmethod
    def transform(obj):
        try:
            if obj == "SecurityAlert":
                obj = "alert"
            elif obj == "SecurityEvent":
                obj = "event"
            elif obj == "SecurityIncident":
                obj = "violation"
        except ValueError:
            LOGGER.error('Cannot convert input %s to finding value', obj)
        return obj


class TimestampConversion(ValueTransformer):
    """ Convert timezone date to timestamp (YYYY-MM-DDThh:mm:ss.000Z)"""
    @staticmethod
    def transform(timestamp):
        try:
            # with milliseconds
            if re.search(r"\d{4}(-\d{2}){2} \d{2}(:\d{2}){2}.\d{0,6}\+\d{2}:\d{2}", str(timestamp)):
                converted_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
                timestamp = datetime.strftime(converted_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            # for without milliseconds, setting three zeroes in the millisecond in the converted date
            elif re.search(r"\d{4}(-\d{2}){2} \d{2}(:\d{2}){2}\+\d{2}:\d{2}", str(timestamp)):
                converted_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S%z")
                timestamp = datetime.strftime(converted_date, "%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
        except:
            LOGGER.error('Cannot convert this timestamp %s', timestamp)
        return timestamp


class ConvertSeverityToScore(ValueTransformer):
    """Transform data source severity to corresponding score value"""
    @staticmethod
    def transform(obj):
        try:
            severity = {"Informational": 25, "Low": 50, "Medium": 75, "High": 100}
            if severity.get(obj):
                obj = severity[obj]
        except ValueError:
            LOGGER.error('Cannot convert input %s to severity score', obj)
        return obj


class ToFloat(ValueTransformer):
    """ Transform the int value to float """
    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, int):
                obj = float(obj)
            return obj
        except ValueError:
            LOGGER.error("Cannot convert input {} to float".format(obj))
