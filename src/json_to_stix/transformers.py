#!/usr/bin/env python3
from . import json_to_stix
from datetime import datetime, timezone
import pprint
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

pp = pprint.PrettyPrinter(indent=2, width=50)


class epochMSToSTIXdt(json_to_stix.valueTransformer):
    """A value transformer for the timestamps"""

    @staticmethod
    def transform(obj):
        return (datetime.fromtimestamp(int(obj) / 1000, timezone.utc)
                .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')


class stringToInteger(json_to_stix.valueTransformer):
    """A value transformer for expected integer values"""

    @staticmethod
    def transform(obj):
        try:
            return int(obj)
        except ValueError:
            print("Can't convert input to integer")
