from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)


class FormatMacAddress(ValueTransformer):
    @staticmethod
    def transform(mac_value):
        """correcting mac address presentation, it should be 6 octate separated
         by only colon (:) not by any other special character """
        mac_value = re.sub("[^A-Fa-f0-9]", "", mac_value)
        mac_length = len(mac_value)
        if mac_length < 12:
            for i in range(mac_length, 12):
                mac_value = "0" + mac_value

        value = ':'.join([mac_value[i:i + 2] for i in range(0, len(mac_value), 2)])
        return value.lower()


class LogscaleToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds"""

    @staticmethod
    def transform(value):
        time_array = value.split('.')
        converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
        return converted_time
