import logging
import unittest
from stix_shifter.stix_translation.src.patterns.translator import translate, DataModels, SearchPlatforms
from .helpers.input_file_helpers import *
from os import listdir, path

logging.basicConfig(level=logging.DEBUG)

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5

default_timerange_spl = '-' + str(DEFAULT_TIMERANGE) + 'minutes'


class TestAnalyticTranslator(unittest.TestCase):
    """ Integration tests for the full pattern conversion process"""
    longMessage = True
    maxDiff = None

    @staticmethod
    def success_test_generator(pattern, search_platform, data_model, expected_result):
        """ Generates a successful test """

        def test(self):
            res = translate(pattern, search_platform, data_model)
            self.assertEqual(normalize_spacing(res['queries'][0]), normalize_spacing(expected_result))
        return test

    @staticmethod
    def failure_test_generator(pattern, search_platform, data_model):
        """ Generates a test for an error """

        def test(self):
            with self.assertRaises(Exception):
                res = translate(pattern, search_platform, data_model)

        return test

    @staticmethod
    def generate_tests():
        """ Generate the tests """

        # for each item in the collected-dict, the key is the test file's name, value is inner dict """
        for k, v in input_files().items():

            # Get the input test file
            test_pattern = v.pop("stix-input")

            # Generate a test for each remaining key in the dictionary
            for platform, expected_result in v.items():
                if '-' in platform and platform != "stix-input":  # Filter out keys that aren't actually platforms
                    dm, sp = platform.split('-')

                    # each test has name in the format: test_md5_hash_car-splunk
                    test_name = "test_{}_{}_{}".format(k, dm, sp)

                    data_model = get_enum_for_input(dm)
                    search_platform = get_enum_for_input(sp)

                    if expected_result is not None:
                        new_test = TestAnalyticTranslator.success_test_generator(test_pattern, search_platform,
                                                                                 data_model, expected_result)
                        setattr(TestAnalyticTranslator, test_name, new_test)
                    else:
                        new_test = TestAnalyticTranslator.failure_test_generator(test_pattern, search_platform,
                                                                                 data_model)
                        setattr(TestAnalyticTranslator, test_name, new_test)


TestAnalyticTranslator.generate_tests()
