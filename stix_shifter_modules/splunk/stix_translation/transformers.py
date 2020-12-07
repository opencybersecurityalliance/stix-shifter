from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer


class SplunkToTimestamp(ValueTransformer):
    """A value transformer for converting Splunk timestamp to regular timestamp"""

    @staticmethod
    def transform(splunkTime):
        return splunkTime[:-6]+'Z'
