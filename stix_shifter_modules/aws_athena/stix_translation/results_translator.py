from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

import os
import json

class ResultsTranslator(JSONToStix):
    # pass
    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)
        hash_algorithm_map = os.path.abspath(os.path.join(base_file_path, "json", "hash_algorithm_map.json"))
        self.hash_names = self.read_json(hash_algorithm_map, options)
        
        network_protocol_path = os.path.abspath(os.path.join(base_file_path, "json", "network_protocol_map.json"))
        self.network_protocol = self.read_json(network_protocol_path, options)
    
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
                    fingerprints_objs =file_obj.get('fingerprints')
                    for fingerprint in fingerprints_objs:
                        hash_name = self.hash_names[str(fingerprint.get('algorithm_id'))]

                        file_obj[hash_name] = fingerprint.get('value')
                        key = "file.hashes.{}".format(hash_name)
                        hash_mapping = {
                            "key": key,
                            "object": "file"
                        }
                        ocsf_map['process']['file'][hash_name] = hash_mapping
            
                # parent_process = process_obj.get('parent_process')
                # if parent_process:
                #     file_obj = parent_process.get('file')
                #     if file_obj:
                #         fingerprints_objs =parent_process.get('fingerprints')
                #         for fingerprint in fingerprints_objs:
                #             hash_name = self.hash_names[str(fingerprint.get('algorithm_id'))]

                #             file_obj[hash_name] = fingerprint.get('value')
                #             key = "file.hashes.{}".format(hash_name)
                #             hash_mapping = {
                #                 "key": key,
                #                 "object": "file"
                #             }
                #             ocsf_map['process']['parent_process']['file'][hash_name] = hash_mapping
            connection_info = ocsf_payload.get('connection_info')
            print(json.dumps(ocsf_payload, indent=4))
            if connection_info:
                if connection_info.get('direction'):
                    connection_info['traffic_direction'] = connection_info.get('direction')

                    protocol_mapping = {
                            "key": "network-traffic.x_direction",
                            "object": "nt"
                    }
                    ocsf_map['connection_info']['traffic_direction'] = protocol_mapping
        # print(json.dumps(ocsf_map['process']['file'],indent=4))
        # print(json.dumps(results, indent=4))
        data = json.dumps(results)
        return super().translate_results(data_source, data)
