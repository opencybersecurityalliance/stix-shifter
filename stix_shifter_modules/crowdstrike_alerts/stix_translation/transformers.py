from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class CrowdStrikeFormatMac(ValueTransformer):
    """A value transformer to convert Mac address to STIX Mac address format"""

    @staticmethod
    def transform(mac):
        value = mac.replace("-", ":")
        return value.lower()