import json

from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.stix_translation.src.utils.exceptions import TranslationResultException


class ResultsTranslator(JSONToStix):

  def __init__(self, options, dialect, base_file_path=None, callback=None):
    super().__init__(options, dialect, base_file_path)

  def translate_results(self, data_source, data):
    results = json.loads(data)
    for result in results:
      if result.get('eventpayload') or result.get('Message'):
        result['mime_type_eventpayload'] = 'text/plain'
      
      if result.get('Message'):
        result['mime_type_message'] = 'text/plain'
      
      if result.get('flowsourcepayload'):
        result['mime_type_flowsourcepayload'] = 'application/octet-stream'
      
      if result.get('flowdestinationpayload'):
        result['mime_type_flowdestinationpayload'] = 'application/octet-stream'

    datasrc = json.loads(data_source)
    try:
      results = json_to_stix_translator.convert_to_stix(datasrc, self.map_data, results, self.transformers, self.options, self.callback)
    except Exception as ex:
      raise TranslationResultException("Error when converting results to STIX: {}".format(ex))
    return results
