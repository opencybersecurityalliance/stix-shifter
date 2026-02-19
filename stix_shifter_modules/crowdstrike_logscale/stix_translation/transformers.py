from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)
connector = __name__.split('.')[1]

class FormatMacAddress(ValueTransformer):
    @staticmethod
    def transform(mac_value):
        """correcting mac address presentation. The mac address should be separated
        by only colon (:) not by any other special character.
        Example:
            Input: 10-10-10-10-10-10  Output: 10:10:10:10:10:10
        """
        try:
            colon_converted = re.sub("[^A-Fa-f0-9]", ":", mac_value)
            return colon_converted.lower()

        except Exception:
            LOGGER.error(f'{connector} connector error -> cannot convert {mac_value} into valid the MAC address')
            raise


class LogscaleToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds
       Example:
           Input : 2024-01-23T12:33:15.170758259Z  Output: 2024-01-23T12:33:15.170Z
    """

    @staticmethod
    def transform(value):
        try:
            time_array = value.split('.')
            converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
            return converted_time
        except Exception:
            LOGGER.error(f'{connector} connector error -> cannot convert {value} into valid timestamp')
            raise
