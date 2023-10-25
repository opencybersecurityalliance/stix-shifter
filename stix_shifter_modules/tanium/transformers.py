from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)

# Add any connector-specific transformers here

class SampleCustomTransformer(ValueTransformer):
    """A sample value transformer to converts some result data element into the required format required by the STIX standard"""

    @staticmethod
    def transform(value): # Keep definition name as is

        try:
            # Do some conversion on the value
            return value
        except ValueError:
            LOGGER.error("Sample error message showing that the conversion failed")