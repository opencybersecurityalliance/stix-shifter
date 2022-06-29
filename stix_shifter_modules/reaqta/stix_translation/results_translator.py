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
                payload['eventName'] = event_name
            
            result['payload'] = self.update_net_traffic_flow(payload)

        data = json.dumps(results)
        return super().translate_results(data_source, data)

    def update_net_traffic_flow(self, payload):
        result_data = payload.get('data')

        if 'protocol' in result_data:
            protocol = self.network_protocol[str(result_data.get('protocol'))]
            result_data['protocol'] = protocol

        if 'outbound' in result_data:
            if not result_data['outbound']:
                temp_local_ip = result_data['localAddr']
                temp_remote_ip = result_data['remoteAddr']
                temp_local_port = result_data['localPort']
                temp_remote_port = result_data['remotePort']
                result_data['localAddr'] = temp_remote_ip
                result_data['remoteAddr'] = temp_local_ip
                result_data['localPort'] = temp_remote_port
                result_data['remotePort'] = temp_local_port
        
        if 'addressFamily' in result_data:
            address_family = result_data.get('addressFamily')
            
            if address_family == 0:
                result_data['addressFamily'] = 'IPv4'
                
                local_addr = result_data['localAddr']
                result_data['localAddrV4'] = local_addr
                del result_data['localAddr']
                
                remote_addr = result_data['remoteAddr']
                result_data['remoteAddrV4'] = remote_addr
                del result_data['remoteAddr']
            elif address_family == 1:
                result_data['addressFamily'] = 'IPv6'

                local_addr = result_data['localAddr']
                result_data['localAddrV6'] = local_addr
                del result_data['localAddr']
                
                remote_addr = result_data['remoteAddr']
                result_data['remoteAddrV6'] = remote_addr
                del result_data['remoteAddr']

        return payload