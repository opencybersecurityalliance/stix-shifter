#!/usr/bin/env python3
from datetime import datetime, timezone


class ValueTransformer():
    """ Base class for value transformers """

    @staticmethod
    def transform(obj):
        """ abstract function for converting value formats """
        raise NotImplementedError


class EpochToTimestamp(ValueTransformer):
    """A value transformer for the timestamps"""

    @staticmethod
    def transform(epoch):
        return (datetime.fromtimestamp(int(epoch) / 1000, timezone.utc)
                .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')


class TimestampToEpoch(ValueTransformer):
    """A value transformer for converting a UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z) to epoch"""

    @staticmethod
    def transform(timestamp):
        time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
        epoch = datetime(1970, 1, 1)
        converted_epoch = int(
            (datetime.strptime(timestamp, time_pattern) - epoch).total_seconds())
        return converted_epoch


class ToInteger(ValueTransformer):
    """A value transformer for expected integer values"""

    @staticmethod
    def transform(obj):
        try:
            return int(obj)
        except ValueError:
            print("Cannot convert input to integer")


class ToString(ValueTransformer):
    """A value transformer for expected string values"""

    @staticmethod
    def transform(obj):
        try:
            return str(obj)
        except ValueError:
            print("Cannot convert input to string")


class ToArray(ValueTransformer):
    """A value transformer for expected array values"""

    @staticmethod
    def transform(obj):
        try:
            obj_array = obj if isinstance(obj, list) else obj.split(', ')
            # Loop through entries inside obj_array and make all strings lowercase to meet STIX format
            obj_array = [entry.lower() for entry in obj_array]
            return obj_array
        except ValueError:
            print("Cannot convert input to array")


def get_all_transformers():
    return {"EpochToTimestamp": EpochToTimestamp, "ToInteger": ToInteger, "ToString": ToString, "ToArray": ToArray}
