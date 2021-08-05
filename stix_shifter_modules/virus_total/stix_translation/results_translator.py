from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import json_to_stix_translator
from os import path
import json
from ipaddress import ip_network, IPv4Network
from stix_shifter_utils.utils import logger

class ResultsTranslator(BaseResultTranslator):

  # Get indicator_types value
  def get_indicator_types(self, value):
    if value == 'safe' or value == 'info':
      return 'benign'
    elif value == 'suspicious':
      return 'anomalous-activity'
    elif value == 'malicious':
      return 'malicious-activity'
    # if key/value pair is not included in the report
    elif value is None:
      return
    else:
      return 'unknown'

  def find_hash_type_by_length(self, value):
    HASH_LENGTH = {'40': 'sha-1', '64': 'sha-256', '32': 'md5'}
    hash_type = HASH_LENGTH.get(str(len(value)), '')
    if hash_type:
      return "file:hashes.'{}'".format(hash_type.upper())
    else:
      return ''

  def get_ip_address(self, ip):
    return 'ipv4' if isinstance(ip_network(ip), IPv4Network) else 'ipv6'

  #return optional fields for indicators such as name, description, indicator-type, kill-chain-phases etc
  def get_optional_values(self, data):        
    # we need 'level' key/value from report.summary.taxonomies[0]
    for ds_key in data:
      if ds_key == "report" and "summary" in data[ds_key] and 'taxonomies' in data[ds_key]['summary']:
        value = data[ds_key]['summary']['taxonomies'][0].get('level')
        indicator_types_value = self.get_indicator_types(value)
        indicator_types = {"indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
        return indicator_types
    return None

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Analyzer result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern

  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "ip", "url", "unknown"],
    if pattern_type == "url":
      pattern = "["+ pattern_type + ":value='" + value + "']"
      return pattern

    elif pattern_type == 'domain':
      pattern = "["+ pattern_type + "-name:value='" + value + "']"
      return pattern
  
    # Get ipv4 or ipv6
    elif pattern_type == 'ip':
      pattern_type = self.get_ip_address(value)
      pattern = "["+ pattern_type + "-addr:value='" + value + "']"
      return pattern

    # Get Hash of type SHA-256, SHA-1, or MD5
    elif pattern_type == 'hash':
      pattern_type = self.find_hash_type_by_length(value)
      pattern = "["+ pattern_type + "='" + value + "']"
      return pattern

    return pattern

  def convert_scans(self, data):
    for key in data:
      if key == "report" and "full" in data[key] and 'scans' in data[key]['full']:
        data[key]['full']['scans'] = [data[key]['full']['scans']]
        return data
    return data
  
  def get_stix_mapping(self):
    json_map = {
      "indicator_types": {
        "key": "indicator_types",
        "cybox": False
      },
      "pattern": {
        "key": "pattern",
        "cybox": False
      },
      "report": {
        "success": {
          "key": "x_original_report.success",
          "cybox": False  
        },
        "summary": {
          "taxonomies": {
            "key": "x_original_report.summary.taxonomies",
            "cybox": False
          }
        },
        "artifacts": {
          "key": "x_original_report.artifacts",
          "cybox": False
        },
        "full": {
          "key": "x_original_report.full",
          "cybox": False
        }
      }
    }
    return json_map

  def nested_mapping(self, map_key, dictionary_key, dictionary_value):
    
    # JSON Dump to convert single quote to double quote and then loads to make it into JSON Dict

    key_string = map_key
    dictionary_value = json.loads(json.dumps(dictionary_value))
    appended_list = [map_key]
    # print("'key': ", key_string)
    if (type(dictionary_value) is dict):
      for val in dictionary_value:
        appended_list.append(self.nested_mapping(key_string + "." + val, val, dictionary_value[val]))
    else:
      # print("ELSE: ", map_key, "DICT KEY: ", dictionary_key, dictionary_value)
      pass
    return appended_list

  def translate_results(self, data_source, data):
    """
    Translates JSON data into STIX results based on a mapping file
    :param data: JSON formatted data to translate into STIX format
    :type data: str
    :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX.
        Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
    :type mapping: str (filepath)
    :return: STIX formatted results
    :rtype: str
    """

    json_data = json.loads(data)
    json_data = json_data[0]
    data_source = json.loads(data_source)
    pattern = self.get_pattern_from_json(json_data)
    optional_indicator_fields = self.get_optional_values(json_data)

    # Append to stix map json
    # Convert to function
    stix_mapping = self.get_stix_mapping()
    json_data['report']['full'] = [json_data['report']['full']]
    self.map_data = stix_mapping

    if optional_indicator_fields is not None:
        json_data = {**optional_indicator_fields, **pattern, **json_data}
    else:
        json_data = {**pattern, **json_data}

    data = json.dumps(json_data)
    data = "[" + data + "]"
    json_data = json.loads(data)
    results = json_to_stix_translator.convert_to_stix_indicator(data_source, self.map_data, json_data, self.transformers, self.options)
    return results
