import re
from datetime import datetime
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer


LOGGER = logger.set_logger(__name__)


class FormatDateTimeObjectToTimestamp(ValueTransformer):
    """A value transformer to convert local datetime object to UTC timestamp"""

    @staticmethod
    def transform(obj):
        try:
            pattern = r'\d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} \(GMT \+\d{2}:\d{2}\)'
            if re.match(pattern, str(obj)):
                obj = datetime.strptime(obj, "%d %b %Y %H:%M:%S (%Z %z)").strftime('%Y-%m-%dT%H:%M:00.000Z')
            return obj
        except ValueError:
            LOGGER.error("Cannot convert value to timestamp format")


class ListToIDTransformer(ValueTransformer):
    """A value transformer to convert list to first index item"""

    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, list) and obj:
                val = obj[0]
                return val
            return int(obj)
        except ValueError:
            LOGGER.error(f"Cannot convert data value {obj} to ID value")


class DictToValueTransformer(ValueTransformer):
    """A value transformer to convert dict to first item value"""

    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, dict) and obj:
                val = list(obj.values())[0]
                return val
            return obj
        except ValueError:
            LOGGER.error(f"Cannot convert data value {obj} to item value")


class ValidateEmailTransformer(ValueTransformer):
    """ Validate email address format """

    @staticmethod
    def transform(obj):
        try:
            pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            if isinstance(obj, list):
                result = []
                for val in obj:
                    if pattern.match(str(val)):
                        result.append(val)
                return result
            elif pattern.match(str(obj)):
                return obj
            return None
        except ValueError:
            LOGGER.error(f"Cannot validate the email {obj}")
