from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
from datetime import datetime

LOGGER = logger.set_logger(__name__)

# Implement custom transformer classes here. 
# The class name needs to be added to the module's to_stix_map.json

class SampleDataTransformer(ValueTransformer):
    """A value transformer to convert <data type> to <transformed format>"""

    @staticmethod
    def transform(data): # Leave method name as is.
        try:
            # add logic to transform data into desired format
            return data
        except ValueError:
            LOGGER.error("Cannot convert data value {} to <transformed format>".format(data))

class timestamp_to_iso_8601(ValueTransformer):
    @staticmethod
    def transform(timestamp):
        try:
            dt = datetime.fromtimestamp(timestamp/1000)
            formatted_time = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            return formatted_time
        except ValueError:
            LOGGER.error("Cannot convert timestamp {} to ISO 8601 format".format(timestamp))
            return timestamp