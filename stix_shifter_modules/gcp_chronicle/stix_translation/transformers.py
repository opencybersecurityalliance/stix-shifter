from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)


class FormatToStixRegistryValue(ValueTransformer):
    """A value transformer to convert gcp chronicle Registry value to windows-registry-key.value STIX"""

    @staticmethod
    def transform(obj):

        try:
            stix_mapping = {"registryValueName": "name", "registryValueData": "data"}
            converted_value = []
            for each_value in obj:
                registryvalue_dict = {}
                for key, value in each_value.items():
                    registryvalue_dict.update({stix_mapping[key]: value})
                converted_value.append(registryvalue_dict)
            return converted_value

        except ValueError:
            LOGGER.error("Cannot convert root value to Stix formatted windows registry value")
            raise


class ValidateUrl(ValueTransformer):
    """ Validate the URL """

    @staticmethod
    def transform(obj):
        pattern = re.compile(
            r"^([a-zA-Z][a-zA-Z0-9+.-]*):(?:\/\/((?:(?=((?:[a-zA-Z0-9-._~!$&'()*+,;=:]|%[0-9a-fA-F]{2})*))(\3)@)?(?=("
            r"(?:\[?(?:::[a-fA-F0-9]+(?::[a-fA-F0-9]+)?|(?:[a-fA-F0-9]+:)+(?::[a-fA-F0-9]+)+|(?:[a-fA-F0-9]+:)+(?::|("
            r"?:[a-fA-F0-9]+:?)*))\]?)|(?:[a-zA-Z0-9-._~!$&'()*+,;=]|%[0-9a-fA-F]{2})*))\5(?::(?=(\d*))\6)?)(\/(?=(("
            r"?:[a-zA-Z0-9-._~!$&'()*+,;=:@\/]|%[0-9a-fA-F]{2})*))\8)?|(\/?(?!\/)(?=((?:[a-zA-Z0-9-._~!$&'()*+,"
            r";=:@\/]|%[0-9a-fA-F]{2})*))\10)?)(?:\?(?=((?:[a-zA-Z0-9-._~!$&'()*+,;=:@\/?]|%[0-9a-fA-F]{2})*))\11)?("
            r"?:#(?=((?:[a-zA-Z0-9-._~!$&'()*+,;=:@\/?]|%[0-9a-fA-F]{2})*))\12)?$")
        if pattern.match(str(obj)):
            return obj
        return None


class FilterValidEmail(ValueTransformer):
    """ Validate email address format """

    @staticmethod
    def transform(obj):
        if isinstance(obj, str):
            email = obj.split(":")
            pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            for em in email:
                if pattern.match(str(em)):
                    return em
            return None
        return obj
