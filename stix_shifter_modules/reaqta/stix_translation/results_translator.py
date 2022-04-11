import os
import json
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

class ResultsTranslator(JSONToStix):
    
    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)

        event_names_path = os.path.abspath(os.path.join(base_file_path, "json", "event_names_map.json"))
        self.event_names = self.read_json(event_names_path, options)
    
    def translate_results(self, data_source, data):
        results = json.loads(data)
        for result in results:
            payload = result['payload']
            if payload.get('eventType'):
                event_name = self.event_names[str(payload.get('eventType'))]
            result['payload']['eventName'] = event_name
        
        data = json.dumps(results, indent=4)
        return super().translate_results(data_source, data)