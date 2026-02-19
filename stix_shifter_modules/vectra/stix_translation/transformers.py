from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger
import re

LOGGER = logger.set_logger(__name__)


class ListToValue(ValueTransformer):
    """A value transformer to return first value from the list"""

    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, list):
                obj = obj[0]
        except ValueError:
            LOGGER.error("Cannot return first value from obj %s", obj)
        return obj


class ChainNameValue(ValueTransformer):
    """A value transformer to add default 'kill_chain_name' as 'mitre-attack' with obj"""

    @staticmethod
    def transform(obj):
        try:
            if obj:
                return [{"kill_chain_name": "mitre-attack","phase_name": obj}]
        except ValueError:
            LOGGER.error("Cannot return obj value %s with default param 'kill_chain_name'", obj)

        return None


class ConvertToReal(ValueTransformer):
    """Transform obj value between 0 to 1 as a float"""

    @staticmethod
    def transform(obj):
        try:
            if not isinstance(obj, float):
                obj = obj / 100
        except ValueError:
            LOGGER.error('Cannot convert input %s to a float value between 0 to 1', obj)
        return obj


class VerifyDomainValue(ValueTransformer):
    """Transform obj value to domain-name"""

    @staticmethod
    def transform(obj):
        try:
            if obj and isinstance(obj, list):
                ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
                domain_pattern = re.compile(r'^(?:(?:[a-z0-9]\.)|(?:[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\.))+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$')
                for index, row in enumerate(obj):
                    if domain_pattern.search(row):
                        continue
                    if ip_pattern.search(row):
                        obj[index] = ip_pattern.search(row).group()
                    else:
                        obj.remove(row)
            if not obj:
                return None
        except ValueError:
            LOGGER.error('Invalid domain value %s', obj)
        return obj
