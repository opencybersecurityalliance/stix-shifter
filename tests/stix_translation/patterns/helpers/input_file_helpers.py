from os import listdir, path
from ..translator import SearchPlatforms, DataModels
import json
import re

MAPPINGS = {
  'cim': DataModels.CIM,
  'car': DataModels.CAR,
  'elastic': SearchPlatforms.ELASTIC,
  'splunk': SearchPlatforms.SPLUNK
}

def input_files():
    """ Collects the test files
        Each input file is a JSON object which contains
        a pattern and the expected results for each platform+language """
    input_patterns = {}  # The input values and expected results

    # do traversal of input_files
    absolute_path_prefix = path.dirname(path.realpath(__file__))  # Find the test directory of filesystem
    for filename in listdir(path.join(absolute_path_prefix, "..", "input_files")):
        name, ext = path.splitext(filename) # reveal pattern name

        with open(path.join(absolute_path_prefix, "..", "input_files", filename), "r") as json_data:
            # add each file's pattern-dict to collected-dict
            input_patterns[name] = json.load(json_data)

    return input_patterns

def normalize_spacing(pattern):
    """ Normalizes spacing across expected results and actual results,
        so you don't need to put newlines/etc to match weird spacing exactly"""
    return re.sub(r"\s+", ' ', pattern).replace("( ", "(").replace(" )", ")")

def collect_targets(input_file):
    """ Collects the set of supported targets, by iterating over the keys
        to figure out which tests are present """

    platforms = set()
    models = set()

    for key in input_file.keys():
        if key not in ['stix-input', 'matches', 'nonmatches']:
            data_model, platform = key.split('-')
            platforms.add(MAPPINGS[platform])

            if data_model in input_file['matches'] or data_model in input_file['nonmatches']:
                models.add(MAPPINGS[data_model])

    return (platforms, models)

def get_enum_for_input(input):
    return MAPPINGS[input]
