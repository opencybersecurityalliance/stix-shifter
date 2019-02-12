""" Miscellaneous tests for specific cases -- tests that are difficult to automate because they apply to handling
edge cases."""

import unittest
from stix_shifter.stix_translation.src.patterns.translator import translate, DataModels, SearchPlatforms
from stix_shifter.stix_translation.src.patterns.errors import SearchFeatureNotSupportedError
import logging
from stix_shifter.utils.error_response import ErrorCode


class TestNotSupported(unittest.TestCase):
    """ Make sure that SearchFeatureNotSupportedErrors are raised appropriately. """
    def test_elastic_followedby(self):
        pattern = "[ipv4-addr:value = '198.51.100.5'] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']"
        result = translate(pattern, SearchPlatforms.ELASTIC, DataModels.CAR)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_NOTSUPPORTED.value == result['code']
        assert result['error'] is not None

