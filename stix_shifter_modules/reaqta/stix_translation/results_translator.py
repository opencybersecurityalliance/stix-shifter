import os
import json
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

class ResultsTranslator(JSONToStix):
    
    def __init__(self, options, dialect, base_file_path=None, callback=None):
        super().__init__(options, dialect, base_file_path, callback)

        event_names_path = os.path.abspath(os.path.join(base_file_path, "json", "event_names_map.json"))
        network_protocol_path = os.path.abspath(os.path.join(base_file_path, "json", "network_protocol_map.json"))
        self.event_names = self.read_json(event_names_path, options)
        self.network_protocol = self.read_json(network_protocol_path, options)
    
    def translate_results(self, data_source, data):
        results = json.loads(data)
        for result in results:
            payload = result['payload']
            if payload.get('eventType'):
                event_name = self.event_names[str(payload.get('eventType'))]
                result['payload']['eventName'] = event_name
            
            result_data = payload.get('data')
            
            if 'protocol' in result_data:
                protocol = self.network_protocol[str(payload['data'].get('protocol'))]
                result['payload']['data']['protocol'] = protocol

            
            if 'addressFamily' in payload['data']:
                address_family = payload['data'].get('addressFamily')
                
                if address_family == 0:
                    payload['data']['addressFamily'] = 'IPv4'
                    
                    local_addr = result['payload']['data']['localAddr']
                    result['payload']['data']['localAddrV4'] = local_addr
                    del result['payload']['data']['localAddr']
                    
                    remote_addr = result['payload']['data']['remoteAddr']
                    result['payload']['data']['remoteAddrV4'] = remote_addr
                    del result['payload']['data']['remoteAddr']
                elif address_family == 1:
                    result['payload']['data']['addressFamily'] = 'IPv6'

                    local_addr = result['payload']['data']['localAddr']

                    result['payload']['data']['localAddrV6'] = local_addr
                    del result['payload']['data']['localAddr']
                    
                    remote_addr = result['payload']['data']['remoteAddr']
                    result['payload']['data']['remoteAddrV6'] = remote_addr
                    del result['payload']['data']['remoteAddr']

        data = json.dumps(results)
        return super().translate_results(data_source, data)