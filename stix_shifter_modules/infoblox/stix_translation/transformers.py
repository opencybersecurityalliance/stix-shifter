# -*- coding: utf-8 -*-
"""
Collection of Transforms to help with the query constructing process.
"""
from datetime import datetime
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class InfobloxToDomainName(ValueTransformer):
    """
    A value transformer for expected domain name

    Required to trim/add `.` to domain names within Infoblox native queries (eg STIX example.com, while Infoblox example.com.)
    """
    @staticmethod
    def transform(url):
        """
        Transforms domainName (removes `.`)

        :param url: dns hostname
        :type url: str
        :return: dns hostname
        :rtype: str
        """
        if url is None:
            return None
        return url.rstrip('.')

    @staticmethod
    def untransform(url):
        """
        Transforms domainName (adds `.`)

        :param url: dns hostname
        :type url: str
        :return: dns hostname
        :rtype: str
        """
        if url is None:
            return None
        return url + '.'

class TimestampToSeconds(ValueTransformer):
    """
    A value transformer for converting a UTC timestamp (YYYY-MM-DDThh:mm:ss.000Z)
    to 10-digit Unix time (epoch + seconds)
    """
    @staticmethod
    def transform(timestamp):
        """
        Transforms timestamp

        :param timestamp: timestamp string
        :type timestamp: str
        :return: converted timestamp
        :rtype: str
        """
        time_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
        epoch = datetime(1970, 1, 1)
        try:
            converted_time = int(((datetime.strptime(timestamp, time_pattern) - epoch).total_seconds()))
            return converted_time
        except ValueError:
            LOGGER.error("Cannot convert the timestamp %s to seconds", timestamp)
        return None
