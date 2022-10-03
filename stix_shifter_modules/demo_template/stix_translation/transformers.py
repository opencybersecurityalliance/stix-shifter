from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

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