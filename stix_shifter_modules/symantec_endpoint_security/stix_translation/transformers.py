import re
from stix_shifter_utils.utils import logger
from datetime import datetime
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_modules.symantec_endpoint_security.stix_translation.query_constructor import \
    QueryStringPatternTranslator

LOGGER = logger.set_logger(__name__)
connector = __name__.split('.')[1]

CONFIG_MAP_PATH = "json/config_map.json"


class TransformerUtil:

    @staticmethod
    def get_mapped_value(attr_name, value, supported_category='enum_supported_values'):
        """
        Retrieves the mapped value from config_map for the specified attribute name and value.
        Args:
            attr_name (str): The name of the attribute for which to retrieve the mapped value.
                            (severity_id, category_id)
            value (str) : The value to be mapped.
            supported_category (str) : supported value type

        Returns:
            str: The mapped value corresponding to the provided attribute name and value
            otherwise as a string value if it does not exist in map.

        Raises:
            ValueError: If the attribute name is not found in the configuration map.
        """
        config_map = QueryStringPatternTranslator.load_json(CONFIG_MAP_PATH)
        attrib_val_dict = config_map[supported_category].get(attr_name)

        if not attrib_val_dict:
            raise ValueError

        inverted_dict = {v: k for k, v in attrib_val_dict.items()}

        if value in inverted_dict:
            return inverted_dict[value]

        return str(value)


class ToSeverityValue(ValueTransformer):
    """
    A value transformer for converting severity_id value
    Example:
        0: 0,
        1: 15
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('severity_id', obj)

            return int(mapped_val)
        except ValueError:
            LOGGER.error("%s connector error, cannot convert severity value : %s", connector, obj)
            raise


class ToCategoryValue(ValueTransformer):
    """
    A value transformer for converting category value
    Example:
        1: "Security",
        2: "License"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('output_category_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert category value : %s", connector, obj)
            raise


class ToOutcomeString(ValueTransformer):
    """
    A value transformer for converting outcome value
    Example:
        1: "Blocked",
        2: "Allowed"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert outcome value : %s", connector, obj)
            raise


class ToStatusString(ValueTransformer):
    """
    A value transformer for converting status Id value
    Example:
        1: "Success",
        2: "Failure"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('status_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert status id value : %s", connector, obj)
            raise


class ToFamilyIdString(ValueTransformer):
    """
    A value transformer for converting family_id value
    Example:
        1: "Container",
        2: "Document"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('family_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert family id value : %s", connector, obj)
            raise


class ToFileContentTypeString(ValueTransformer):
    """
    A value transformer for converting severity value
    Example:
        1: "Application",
        2: "Binary"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('file.content_type.type_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert content type id value : %s", connector, obj)
            raise


class ToFileTypeString(ValueTransformer):
    """
    A value transformer for converting severity value
    Example:
        1: "File",
        2: "Directory"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('file.type_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert file type value : %s", connector, obj)
            raise


class ToFindingTypeString(ValueTransformer):
    """
    A value transformer for converting severity value
    Example:
        1: "policy",
        2: "threat"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('reason_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert finding type value : %s", connector, obj)
            raise


class ToFindingSeverityString(ValueTransformer):
    """
    A value transformer for converting severity value
    Example:
        100: 100,
        200: 80
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('threat.risk_id', obj)

            return int(mapped_val)
        except ValueError:
            LOGGER.error("%s connector error, cannot convert finding severity value : %s", connector, obj)
            raise


class ToThreatTypeString(ValueTransformer):
    """
    A value transformer for converting severity value
    Example:
        1: "Malware",
        2: "Behavioral"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('threat.type_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert threat type value : %s", connector, obj)
            raise


class ToDeviceOsTypeString(ValueTransformer):
    """
    A value transformer for converting Device Os Type id value
    Example:
        100: "Windows"
        200: "Linux"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('device_os_type_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert Device OS type value : %s", connector, obj)
            raise


class ToDirectionString(ValueTransformer):
    """
    A value transformer for converting direction_id value
    Example:
        0: "Unknown"
        1: "Inbound"
        2: "Outbound"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('connection.direction_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert direction_id value : %s", connector, obj)
            raise


class ToKernelType(ValueTransformer):
    """
    A value transformer for converting kernel type_id value
    Example:
        0: "Unknown"
        1: "Shared mutex"
        2: "System call"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('kernel.type_id', obj)

            return mapped_val
        except ValueError:
            LOGGER.error("%s connector error, cannot convert kernel type_id value : %s", connector, obj)
            raise


class ToProtocolKeyWord(ValueTransformer):
    """
    A value transformer for converting protocol decimal value to keyword value
    Example:
        6: "tcp"
        17: "udp"
    """

    @staticmethod
    def transform(obj):
        try:
            mapped_val = TransformerUtil.get_mapped_value('connection.protocol_id', obj, 'protocol_supported_values')

            return [mapped_val]
        except ValueError:
            LOGGER.error("%s connector error, cannot convert protocol decimal value : %s", connector, obj)
            raise


class ToFormatMac(ValueTransformer):

    """A value transformer to convert Mac address to STIX Mac address format.
    Example:
        "12:5A:DE:E5:84:E5"
    """

    @staticmethod
    def transform(obj):
        try:
            return obj.lower()
        except ValueError:
            LOGGER.error("%s connector error, cannot convert mac value : %s", connector, obj)
            raise


class TimestampToAddMilliseconds(ValueTransformer):
    """
    A value transformer for adding milliseconds if not present in value.
    Example:
        input: ""2024-05-03T04:27:56Z"
        output: "2024-05-03T04:27:56.000Z"
    """

    @staticmethod
    def transform(timestamp):
        try:
            # Regular expression pattern to match th format '%Y-%m-%dT%H:%M:%SZ' without milli seconds
            if re.match(r"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}Z", str(timestamp)):
                dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                timestamp = datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            return timestamp
        except ValueError:
            LOGGER.error(f"Cannot convert the timestamp {timestamp} to add milliseconds")


class ToListValue(ValueTransformer):
    """A value transformer that converts a single value into a list."""

    @staticmethod
    def transform(obj):
        if not isinstance(obj, list):
            obj = [obj]
        return obj

class ToAlgorithmHashes(ValueTransformer):
    """A value transformer that converts hashes to stix hashes format.
    Example:
        input : [{"algorithm": "sha1", "value": "21EE32614E2EE32EEE9E2056EEE28EEE5E7EEEEA"}]
        output: {"sha1": "21EE32614E2EE32EEE9E2056EEE28EEE5E7EEEEA"}
    """

    @staticmethod
    def transform(obj):
        try:
            if isinstance(obj, list):
                obj = {item["algorithm"]: item["value"] for item in obj}
            return obj
        except ValueError:
            LOGGER.error(f"Cannot convert the hashes {obj} to hashes format")
