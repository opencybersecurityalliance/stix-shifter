import unittest
import json

from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_modules.stix_bundle.entry_point import EntryPoint


class TestResultsTranslator(unittest.TestCase, object):
    DATA_SOURCE = {
        "type": "identity",
        "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
        "name": "stix_bundle",
        "identity_class": "events"
    }

    def test_results_translation(self):
        result_file = open(
            'stix_shifter_modules/stix_bundle/test/qradar_observed_2000.json', 'r').read()
        data = json.loads(result_file)
        result_bundle_objects = data['objects']
        observed_data = result_bundle_objects[1]

        entry_point = EntryPoint()
        result_bundle = run_in_thread(
            entry_point.translate_results, self.DATA_SOURCE, [observed_data])
        final_bundle_objects = result_bundle['objects'][1]
        assert observed_data == final_bundle_objects