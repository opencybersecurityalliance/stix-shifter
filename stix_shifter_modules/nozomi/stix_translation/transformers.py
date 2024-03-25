import re
from stix_shifter_utils.utils import logger
from datetime import datetime, timezone
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer

LOGGER = logger.set_logger(__name__)
connector = __name__.split('.')[1]


class ChainNameValue(ValueTransformer):
    """A value transformer to add default 'kill_chain_name' as 'mitre-attack' with obj"""

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
    """Regex to check valid MAC address"""

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
    """A value transformer for expected finding_type value"""

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
    """A value transformer for converting severity value"""

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
            LOGGER.error("%s connector error, cannot convert input : %s", connector, obj)
            raise


class SizeToInteger(ValueTransformer):
    """A value transformer for converting value to integer value"""

    @staticmethod
    def transform(obj):
        try:
            if obj:
                return int(str(obj).replace(" bytes", ""))
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert input : %s", connector, obj)
            raise


class ToProtocolValue(ValueTransformer):
    """A value transformer for converting value to protocol value"""

    @staticmethod
    def transform(obj):
        try:
            if obj:
                if '/' in obj:
                    protocol = obj.split("/")[0]
                    return [protocol]
                if obj == 'unknown':
                    return ['tcp']
                return [obj.lower()]
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert input : %s", connector, obj)
            raise


class EpochToTimestampConversion(ValueTransformer):
    """A value transformer for the 13-digit timestamps"""

    @staticmethod
    def transform(obj):
        try:
            if obj:
                return datetime.fromtimestamp(int(obj)/1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return None
        except ValueError:
            LOGGER.error("%s connector error, cannot convert epoch value %s to timestamp", connector, obj)
