from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
from datetime import timezone
LOGGER = logger.set_logger(__name__)


class FormatDateTimeObjectToTimestamp(ValueTransformer):
    """A value transformer to convert local datetime object to UTC timestamp"""

    @staticmethod
    def transform(obj):

        try:
            if not isinstance(obj, str):
                utc_timestamp_str = obj.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                return utc_timestamp_str
            return obj

        except ValueError:
            LOGGER.error("Cannot convert root value to timestamp format")
            raise
