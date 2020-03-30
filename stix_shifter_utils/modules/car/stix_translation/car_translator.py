
from stix_shifter_utils.modules.base.stix_translation.base_translator import BaseTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from os import path
import json


class CARToStix(JSONToStix):

  def __init__(self, dialect=None, callback=None):
    basepath = path.dirname(__file__)
    filepath = path.abspath(
        path.join(basepath, "json", "to_stix_map.json"))
    self.default_mapping_file_path = filepath
    self.callback=None

  def translate_results(self, data_source, data, options, mapping=None):
      """
      Translates JSON data into STIX results based on a mapping file
      :param data: JSON formatted data to translate into STIX format
      :type data: str
      :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX. Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
      :type mapping: str (filepath)
      :return: STIX formatted results
      :rtype: str
      """

      json_data = json.loads(data)
      for obj in json_data:
        typ = obj.pop('object', '')
        fields = obj.pop('fields', [])
        for field in fields:
          obj[f"{typ}.{field}"] = fields[field]

      return JSONToStix.translate_results(self, data_source, json.dumps(json_data), options, mapping)

