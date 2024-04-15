import re
from stix_shifter_utils.utils import logger
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.stix_translation.src.utils.transformers import EpochToTimestamp

LOGGER = logger.set_logger(__name__)
connector = __name__.split('.')[1]


class ChainNameValue(ValueTransformer):
    """A value transformer to add default 'kill_chain_name' as 'mitre-attack' with obj
    Example:
        Input: 'Command and Control'
        Output: [{'kill_chain_name': 'mitre-attack', 'phase_name': 'Command and Control'}]
    """
    @staticmethod
    def transform(obj):
        try:
            if obj:
                return [{"kill_chain_name": "mitre-attack", "phase_name": obj}]
        except ValueError:
            LOGGER.error("%s connector error, cannot return obj value %s with default param 'kill_chain_name'",
                         connector, obj)
        return None


class ValidateMacAddr(ValueTransformer):
    """Regex to check valid MAC address
    Example:
        Input: Invalid mac address
        Output: None
    """
    @staticmethod
    def transform(obj):
        try:
            pattern = re.compile(r'^(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})|([0-9a-fA-F]{3}[\.]){3}([0-9a-fA-F]{3}))$')
            if re.search(pattern, str(obj)):
                return obj
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot validate mac address: %s", connector, obj)
            raise


class ToFindingType(ValueTransformer):
    """A value transformer for expected finding_type value
    Example:
        Input: empty string or other than empty string
        Output: alert or threat
    """
    @staticmethod
    def transform(obj):
        try:
            if obj in ("", "alert"):
                return "alert"
            return "threat"
        except ValueError:
            LOGGER.error("%s connector error, cannot convert input to finding type : %s", connector, obj)
            raise


class ToSeverityValue(ValueTransformer):
    """A value transformer for converting severity value
    Example:
        Input: 9.0 or 9 or '9.0'
        Output: 90
    """
    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, (float, int)):
                return int(obj * 10)
            if obj.isnumeric():
                return int(obj) * 10
            if obj.replace(".", "").isnumeric():
                return int(float(obj) * 10)
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert field into a severity rating : %s", connector, obj)
            raise


class SizeToInteger(ValueTransformer):
    """A value transformer for converting value to integer value
    Example:
        Input: '19261 bytes'
        Output: 19261
    """
    @staticmethod
    def transform(obj):
        try:
            if obj:
                return int(str(obj).replace(" bytes", ""))
            return None
        except ValueError:
            LOGGER.error("%s connector error, failed to convert byte size to integer : %s", connector, obj)
            raise


class ToProtocolValue(ValueTransformer):
    """A value transformer for converting value to protocol value
    Example:
        Input: 'tcp/3389' or 'unknown'
        Output: [tcp] or [tcp]
    """
    @staticmethod
    def transform(obj):
        try:
            if obj:
                if '/' in obj:
                    protocol = obj.split("/")[0].lower()
                    return [protocol]
                if obj == 'unknown':
                    return None
                return [obj.lower()]
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert input into protocol value : %s", connector, obj)
            raise


class EpochToTimestampConversion(ValueTransformer):
    """A value transformer for the 13-digit timestamps with check on input value
    Example:
        Input: 1698836400000
        Output: '2023-11-01T11:00:00.000Z'
    """
    @staticmethod
    def transform(obj):
        try:
            if obj:
                return EpochToTimestamp.transform(obj)
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert epoch value %s to timestamp", connector, obj)
