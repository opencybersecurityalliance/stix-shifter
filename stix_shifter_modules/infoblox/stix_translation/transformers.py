# -*- coding: utf-8 -*-
from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class InfobloxToDomainName(ValueTransformer):
    """A value transformer for expected domain name"""

    @staticmethod
    def transform(url):
        if url is None:
            return
        return url.rstrip('.')

    @staticmethod
    def untransform(url):
        if url is None:
            return
        return url + '.'

