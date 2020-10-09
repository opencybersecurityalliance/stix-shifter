from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer


class AwsToTimestamp(ValueTransformer):
    """
    A value transformer for converting AWS timestamp (YYYY-MM-DD hh:mm:ss.000)
    to UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z)
    """

    @staticmethod
    def transform(aws_time):
        time_array = aws_time.split(' ')
        converted_time = time_array[0] + 'T' + time_array[1] + 'Z'
        return converted_time
