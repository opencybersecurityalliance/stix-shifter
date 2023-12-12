from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re
from datetime import datetime


LOGGER = logger.set_logger(__name__)


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
                timestamp = datetime.strftime(converted_date, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        except:
            LOGGER.error('Cannot convert this timestamp %s', timestamp)
        return timestamp


class SeverityToScore(ValueTransformer):

    @staticmethod
    def transform(severity):
        """
        sysdig severity values levels 1-10 :
        High: 0-3, Medium: 4-5, Low: 6, Info: 7-10
        converting sysdig severity values 1-10 to 1-100
        Example :
            High: sysdig severity : 0, after conversion : 100
            Low : sysdig severity : 6, after conversion : 40
        """
        try:
            # value transformer to convert severity value on a scale of 1-100
            if isinstance(severity, int):
                return (10 - int(severity)) * 10
            return severity
        except KeyError:
            LOGGER.error("Cannot convert severity scale value")


class HostnameToIpAddress(ValueTransformer):
    """
    Converts Node Name into IP address
    """
    @staticmethod
    def transform(address):
        try:
            match = re.search(r'\d+\-\d+\-\d+\-\d+', address)
            if match:
                # Getting the matched IP address
                extracted_ip = match.group()
                return extracted_ip.replace('-', '.')
            return address
        except KeyError:
            LOGGER.error("Cannot convert ip value")
