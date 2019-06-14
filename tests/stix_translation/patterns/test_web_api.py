import unittest
from multiprocessing import Process
import os

from web_api import *
from .helpers.input_file_helpers import *

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
default_timerange_spl = '-' + str(DEFAULT_TIMERANGE) + 'minutes'


class TestRunFlask(unittest.TestCase):
    """ Test the Flask server for Analytic Translator
        expects input files in test/input_files/ """

    @classmethod
    def setUpClass(cls):
        cls.server = Process(target=run_server)
        cls.server.start()
        app.testing = True
        return "Starting Flask server..."

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.join()
        return "Flask Server shutting down..."

    @staticmethod
    def success_test_generator(pattern, platform, expected_result):
        """ Generates a successful test """

        def test(self):
            with app.test_client() as client:
                resp = client.post(platform, data=pattern, content_type='text/plain')
                data = resp.data
                print("\n DATA: ", data.decode("utf-8"))  # TEST-PRINT
                self.assertEqual(TestRunFlask.normalize_spacing(data.decode("utf-8")),
                                 TestRunFlask.normalize_spacing(expected_result))
        return test

    @staticmethod
    def failure_test_generator(pattern, platform):
        """ Generates a test for an error """

        def test(self):
            with self.assertRaises(Exception):
                with app.test_client() as client:
                    resp = client.post(platform, data=pattern, content_type='text/plain')
                    data = resp.data
                    print("\n DATA: ", data.decode("utf-8"))  # TEST-PRINT
        return test

    def normalize_spacing(pattern):
        """ Normalizes spacing across expected results and actual results,
        so you don't need to put newlines/etc to match weird spacing exactly"""
        return re.sub(r"\s+", ' ', pattern)

    @staticmethod
    def input_files():
        """ Collects the test files
            Each input file is a JSON object which contains
            a pattern and the expected results for each platform+language """
        input_patterns = {}  # The input values and expected results
        absolute_path_prefix = os.path.dirname(os.path.realpath(__file__))
        # do traversal of input_files
        for filename in listdir(path.join(absolute_path_prefix, "input_files")):
            name, ext = path.splitext(filename)  # reveal pattern name
            with open(path.join(absolute_path_prefix, "input_files", filename), "r") as json_data:
                # add each file's pattern-dict to collected-dict
                input_patterns[name] = json.load(json_data)
        return input_patterns

    @staticmethod
    def generate_tests():
        """ Generate the tests """

        # For now, supported platforms are combined with data models
        # TODO: This will be split when the refactor is merged
        platform_map = {
            'car-elastic': (DataModels.CAR, SearchPlatforms.ELASTIC),
            'car-splunk': (DataModels.CAR, SearchPlatforms.SPLUNK)
        }

        # for each item in the collected-dict,
        #   the key is the test file's name,
        #   the value is inner dict
        for k, v in TestRunFlask.input_files().items():

            # Get the input test file
            test_pattern = v.pop("stix-input")

            # Generate a test for each remaining key in the dictionary
            for platform, expected_result in v.items():

                # each test is named in format: test_stg_md5_hash_car-splunk
                # test_name = "test_[GENERATOR]_{}_{}".format(k, platform)
                if platform in platform_map:  # Some platforms not yet supported
                    if expected_result is not None:
                        test_name = "test_stg_{}_{}".format(k, platform)
                        new_test = TestRunFlask.success_test_generator(
                            test_pattern, platform, expected_result)
                        setattr(TestRunFlask, test_name, new_test)
                    else:
                        test_name = "test_ftg_{}_{}".format(k, platform)
                        new_test = TestRunFlask.failure_test_generator(
                            test_pattern, platform)
                        setattr(TestRunFlask, test_name, new_test)


TestRunFlask.generate_tests()
