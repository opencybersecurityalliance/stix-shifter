import json

from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from .splunk_utils import hash_type_lookup

class ResultsTranslator(JSONToStix):
  
  def __init__(self, options, dialect, base_file_path=None, callback=None):
    super().__init__(options, dialect, base_file_path, hash_type_lookup)

  def translate_results(self, data_source, data):
    results = json.loads(data)
    for result in results:
      if result.get('_raw'):
        result['mime_type_raw'] = 'text/plain'
    
    data = json.dumps(results, indent=4)

    return super().translate_results(data_source, data)