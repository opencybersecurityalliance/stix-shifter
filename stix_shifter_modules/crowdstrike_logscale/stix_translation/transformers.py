from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)


class FormatMacAddress(ValueTransformer):
    @staticmethod
    def transform(mac_value):
        """correcting mac address presentation. The mac address should be separated
        by only colon (:) not by any other special character """
        colon_converted = re.sub("[^A-Fa-f0-9]", ":", mac_value)
        return colon_converted.lower()


class LogscaleToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds"""

    @staticmethod
    def transform(value):
        time_array = value.split('.')
        converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
        return converted_time
