from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class ConvertHexToInteger(ValueTransformer):
    @staticmethod
    def transform(obj: str):
        try:
            return int(obj, 16)
        except ValueError:
            LOGGER.error("Cannot convert hex string to integer")
