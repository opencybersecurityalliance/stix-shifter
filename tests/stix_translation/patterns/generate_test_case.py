"""
This file will automatically generate tests from the .json in input_files/ .  (Useful if you have an IDE and like to
right-click to run tests).
"""
import os
import json

def escape_double_quotes(pattern: str):
    return pattern.replace('"', '\\"')

if __name__ == '__main__':
    patterns = {}

    absolute_path_prefix = os.path.dirname(os.path.realpath(__file__))  # Find the test directory of filesystem
    for json_file in os.listdir(os.path.join(absolute_path_prefix, 'input_files')):
        with open(os.path.join(absolute_path_prefix, 'input_files', json_file), 'r') as jfp:
            pattern = json.load(jfp)
            patterns[json_file.rstrip('.json')] = pattern['stix-input']

    file_header = """
import unittest
from stix_shifter.stix_translation.src.patterns.translator import translate, DataModels, SearchPlatforms
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class TextStix2PatterningInput(unittest.TestCase):"""

    prototype_test_case = """
    def test_{pattern_name}(self):
        res = {test_function}("{pattern}", {search_platform}, {data_model})
        print("CONVERTED: {pattern}    TO   ", res)
    """
    search_platforms = {"elastic": "SearchPlatforms.ELASTIC",
                        "splunk": "SearchPlatforms.SPLUNK"}
    data_models = {"car": "DataModels.CAR",
                   "cim": "DataModels.CIM"}
    with open(os.path.join(absolute_path_prefix, "generated_tests.py"), 'w') as test_file:
        test_file.write(file_header)

        # STIX2 Native parser and CAR DataModel tests (can add more later).
        for name, pattern in patterns.items():
            for search_name, search_platform in search_platforms.items():
                for dm_name, data_model in data_models.items():
                    test_file.write(prototype_test_case.format(pattern_name="_".join([name, dm_name, search_name]),
                                                               test_function="translate",
                                                               search_platform=search_platform,
                                                               data_model=data_model,
                                                               pattern=escape_double_quotes(pattern)))
