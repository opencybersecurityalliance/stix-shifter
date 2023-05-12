import json

from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

class ResultsTranslator(JSONToStix):

  def __init__(self, options, dialect, base_file_path=None, callback=None):
    super().__init__(options, dialect, base_file_path)

  def translate_results(self, data_source, data):
    results = data
    for result in results:
      if result.get('eventpayload') or result.get('Message'):
        result['mime_type_eventpayload'] = 'text/plain'
      
      if result.get('Message'):
        result['mime_type_message'] = 'text/plain'
      
      if result.get('flowsourcepayload'):
        result['mime_type_flowsourcepayload'] = 'application/octet-stream'
      
      if result.get('flowdestinationpayload'):
        result['mime_type_flowdestinationpayload'] = 'application/octet-stream'

      if result.get('sourceip'):
        if result['sourceip'] == '0.0.0.0':
          result['sourceip'] = None

      if result.get('destinationip'):
        if result['destinationip'] == '0.0.0.0':
          result['destinationip'] = None

      if result.get('sourcemac'):
        if result['sourcemac'] == '00:00:00:00:00:00' or result['sourcemac'] == '00-00-00-00-00-00':
          result['sourcemac'] = None

      if result.get('destinationmac'):
        if result['destinationmac'] == '00:00:00:00:00:00' or result['destinationmac'] == '00-00-00-00-00-00':
          result['destinationmac'] = None

      if result.get('identityip'):
        if result['identityip'] == '0.0.0.0':
          result['identityip'] = None

      if result.get('sourcev6'):
        if result['sourcev6'] == '0:0:0:0:0:0:0:0':
          result['sourcev6'] = None

      if result.get('destinationv6'):
        if result['destinationv6'] == '0:0:0:0:0:0:0:0':
          result['destinationv6'] = None

    return super().translate_results(data_source, results)