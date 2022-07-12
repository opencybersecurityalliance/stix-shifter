from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class FormatToStixRegistryValue(ValueTransformer):
    """A value transformer to convert paloalto Registry value to windows-registry-key.value STIX"""

    @staticmethod
    def transform(registry):

        try:
            return [{'name': registry}]
        except ValueError:
            LOGGER.error("Cannot convert root value to Stix formatted windows registry value")
