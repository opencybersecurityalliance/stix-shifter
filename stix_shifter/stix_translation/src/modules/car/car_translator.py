
# ..base.base_translator import BaseTranslator
from ..base.base_translator import BaseTranslator
from ...json_to_stix.json_to_stix import JSONToStix
from ..base.base_query_translator import BaseQueryTranslator
from os import path
import json


class CARToStix(JSONToStix):
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

class Translator(BaseTranslator):

    def __init__(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", "to_stix_map.json"))
        self.mapping_filepath = filepath
        self.result_translator = CARToStix(filepath)
        self.query_translator = None
