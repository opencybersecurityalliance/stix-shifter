from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class SeverityToScore(ValueTransformer):
    """value transformer to convert severity string value to integer value on a scale of 1-100"""

    @staticmethod
    def transform(severity):

        severity_string_to_integer = {"LOW_SEVERITY": 25,
                                      "MEDIUM_SEVERITY": 50,
                                      "HIGH_SEVERITY": 75,
                                      "CRITICAL_SEVERITY":100
                                      }

        try:
            return severity_string_to_integer[severity]

        except KeyError:
            LOGGER.error("Cannot convert string to severity scale value")


class ToIsactive(ValueTransformer):
    """value transformer to convert inactive value to Isactive value """

    @staticmethod
    def transform(inactive):

        if (isinstance(inactive, bool)):
            isactive = not inactive
        else:
            isactive = False

        return isactive
