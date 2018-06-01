#!/usr/bin/env python3
from .json_to_stix_translator import ValueTransformer
from datetime import datetime, timezone


class EpochToStix(ValueTransformer):
    """A value transformer for the timestamps"""

    @staticmethod
    def transform(epoch):
        return (datetime.fromtimestamp(int(epoch) / 1000, timezone.utc)
                .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')


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


def get_all_transformers():
    return {"EpochToStix": EpochToStix, "ToInteger": ToInteger, "ToString": ToString}
