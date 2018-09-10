""" Miscellaneous tests for specific cases -- tests that are difficult to automate because they apply to handling
edge cases."""

import unittest
from stix_shifter.src.patterns.translator import translate, DataModels, SearchPlatforms
from stix_shifter.src.patterns.errors import SearchFeatureNotSupportedError
import logging


class TestNotSupported(unittest.TestCase):
    """ Make sure that SearchFeatureNotSupportedErrors are raised appropriately. """
    def test_elastic_followedby(self):
        pattern = "[ipv4-addr:value = '198.51.100.5'] FOLLOWEDBY [ipv4-addr:value = '198.51.100.10']"
        with self.assertRaises(SearchFeatureNotSupportedError):
            res = translate(pattern, SearchPlatforms.ELASTIC, DataModels.CAR)
