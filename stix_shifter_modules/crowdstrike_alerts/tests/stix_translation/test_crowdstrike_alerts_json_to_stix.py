import os
from stix_shifter_utils.utils.async_utils import run_in_thread
from stix_shifter_modules.crowdstrike_alerts.entry_point import EntryPoint
import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

entry_point = EntryPoint()
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "crowdstrike_alerts",
    "identity_class": "events"
}
options = {}


class TestCrowdStrikeAlertsTransformResults(unittest.TestCase, object):
  
  @staticmethod
  def get_untranslated_results_file():    
    if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_data.json"):
      with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_data.json", "r") as file:
        return json.load(file)
      
  @staticmethod
  def get_translated_results_file():    
    if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_transformed.json"):
      with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_transformed.json", "r") as file:
        return json.load(file)
      
  @staticmethod
  def write_to_translated_results_file(data):    
    if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_transformed.json"):      
      with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_results_transformed.json", "w") as file:
        json.dump(data, file)
  
  def test_change_crowdstrike_process_api_timestamp_regex(self):
    untranslated_results = TestCrowdStrikeAlertsTransformResults.get_untranslated_results_file()
    translated_results = TestCrowdStrikeAlertsTransformResults.get_translated_results_file()
    
    result_bundle = run_in_thread(entry_point.translate_results, data_source, untranslated_results["data"])

    result_bundle_objects = []
    translated_results_objects = []
    for result in result_bundle["objects"][1:]:
      result_bundle_objects.append(result["objects"])
      
    for result in result_bundle["objects"][1:]:
      translated_results_objects.append(result["objects"])
      
    assert result_bundle_objects == translated_results_objects
    
    
    
    