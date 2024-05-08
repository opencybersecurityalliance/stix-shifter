import os
import json

from stix_shifter_utils.utils.file_helper import read_json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseJsonSyncConnector):
    # LOOKS LIKE MAX COUNT is 500. response doesn't show why it fails
    MAX_LIMIT = 500
    
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
    
    async def ping_connection(self):
        return_obj = dict()
        response_dict = dict()
        try:
            response = await self.api_client.ping_data_source()
            response_code = response['code']
            
            if response_code == 200:
                return_obj['success'] = True
            elif response_code == 401:
                response_dict['type'] = 'AuthenticationError'
                response_dict['message'] = 'Invalid App Secret key provided. {}'.format(response['message'])
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                response_dict['type'] = 'AuthenticationError'
                response_dict['message'] = 'Invalid App ID provided. {}'.format(response['message'])
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except ConnectionError as ex:
            self.logger.error('error when pinging datasource {}:'.format(ex))
            response_dict['type'] = 'ConnectionError'
            response_dict['message'] = 'Invalid hostname provided. {}'.format(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            self.logger.error('error when pinging datasource {}:'.format(ex))
            response_dict['type'] = 'AuthenticationError'
            response_dict['message'] = 'Authentication Failure. API Response: {}'.format(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        
        return return_obj
    
    async def create_results_connection(self, search_id, offset, length):  
        return_obj = dict()
        length = int(length)
        offset = int(offset)
        total_records = offset + length

        try:
            if total_records <= self.MAX_LIMIT:
                # Grab the response, extract the response code, and convert it to readable json
                response = await self.api_client.get_search_results(search_id, length)
            elif total_records > self.MAX_LIMIT:
                response = await self.api_client.get_search_results(search_id, self.MAX_LIMIT)
            
            response_code = response.code
            response_text = response.read()
            try:
                response_dict = json.loads(response_text)
            except ValueError as ex:
                self.logger.debug(response_text)
                error = Exception(f'Can not parse response from reaqta. The response is not a valid json: {response_text} : {ex}')
            
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['result']
                while len(return_obj['data']) < total_records:
                    remainings = total_records - len(return_obj['data'])
                    try:
                        next_page_url = response_dict['nextPage']
                        if next_page_url:
                            response = await self.api_client.page_search(search_id, next_page_url, remainings)
                            response_code = response.code
                            response_dict = json.loads(response.read())
                            if response_code == 200:
                                return_obj['data'].extend(response_dict['result'])
                        else:
                            break
                    except Exception as ex:
                        raise ex
                data = return_obj['data'][offset:total_records]
                Connector.modify_result(data)
                return_obj['data'] = data
            elif response_code == 422:
                error_string = 'query_syntax_error: ' + response_dict['message']
                ErrorResponder.fill_error(return_obj, error_string, ['message'], connector=self.connector)
            else:
                error_string = 'query_syntax_error: ' + response_dict['message']
                ErrorResponder.fill_error(return_obj, error_string, ['message'], connector=self.connector)
            
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(str(err)))
            ErrorResponder.fill_error(return_obj, err, ['message'], connector=self.connector)
        
        return return_obj
    
    @classmethod
    def modify_result(cls, data):
        #For whatever reason, the api does not return the name of the Tactic, just an ID that maps loosely to a few tactics.
        #This is a mapping of the UI useful name with the internal ID they are using.
        #I determined this by using their HunQ search tool within the Reaqta environment.
        #This could change in the future and may need to be updated or removed.
        tactic_name_mapping = {
            0:"Unknown",
            1:"Initial Access",
            2:"Execution",
            3:"Persistence",
            4:"Privilege Escalation",
            5:"Defense Evasion",
            6:"Credential Access",
            7:"Discovery",
            8:"Lateral Movement",
            9:"Collection",
            10:"Command and Control",
            11:"Exfiltration",
            12:"Impact"
        }
        
        
        transmit_basepath = os.path.abspath(__file__)
        translate_basepath = transmit_basepath.split(os.sep)
        event_names_path = os.sep.join([*translate_basepath, "stix_translation", "json", "event_names_map.json"])
        network_protocol_path = os.sep.join([*translate_basepath, "stix_translation", "json", "network_protocol_map.json"])
        
        # network_protocol_path = os.path.abspath(os.path.join(translate_basepath, "json", "network_protocol_map.json"))
        event_names = read_json(event_names_path, options={})
        network_protocol = read_json(network_protocol_path, options={})
        print(data)
        for result in data:
            if result.get('payload'):
                payload = result['payload']
                if payload.get('eventType'):
                    event_name = event_names[str(payload.get('eventType'))]
                    payload['eventName'] = event_name
                
                result['payload'] = cls.update_net_traffic_flow(payload, network_protocol)
            
            if result.get('payload') and result['payload'].get('data') and result['payload']['data'].get('tactics'):
                tactic_list = result['payload']['data']['tactics']
                technique = result['payload']['data']['technique']
                result['payload']['data']['mod_tactics'] = {}
                dict_list = []
                for tactic in tactic_list:
                    
                    if (tactic in tactic_name_mapping):
                        dict_list.append({"tactic_number": tactic, "tactic_name": tactic_name_mapping.get(tactic), "technique":technique})
                    else:
                        dict_list.append({"tactic_number": tactic, "tactic_name": "Unknown", "technique":technique})
                result['payload']['data']['mod_tactics'] = dict_list
                
                
    @classmethod
    def update_net_traffic_flow(cls, payload, network_protocol):
        result_data = payload.get('data')

        if 'protocol' in result_data:
            protocol = network_protocol[str(result_data.get('protocol'))]
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
