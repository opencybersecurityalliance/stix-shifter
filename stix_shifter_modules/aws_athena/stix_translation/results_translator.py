from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

import os
import json

class ResultsTranslator(JSONToStix):
    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)
        hash_algorithm_map = os.path.abspath(os.path.join(base_file_path, "json", "hash_algorithm_map.json"))
        self.hash_names = self.read_json(hash_algorithm_map, options)

    def translate_results(self, data_source, data):
        mappping = self.map_data
        ocsf_map = mappping['ocsf']
        results = json.loads(data)
        for result in results:
            ocsf_payload = result['ocsf']
            process_obj = ocsf_payload.get('process')
            if process_obj:
                file_obj = process_obj.get('file')
                if file_obj:
                    file_obj['hashes'] = self.update_hash_mapping(file_obj)
            
                parent_process = process_obj.get('parent_process')
                if parent_process:
                    file_obj = parent_process.get('file')
                    if file_obj:
                        file_obj['hashes'] = self.update_hash_mapping(file_obj)
  
        data = json.dumps(results)
        return super().translate_results(data_source, data)

    def update_hash_mapping(self, file_obj):
        hashes = {}
        fingerprints_objs =file_obj.get('fingerprints')
        
        for fingerprint in fingerprints_objs:
            hash_name = self.hash_names[str(fingerprint.get('algorithm_id'))]

            hashes[hash_name] = fingerprint.get('value')

        return hashes