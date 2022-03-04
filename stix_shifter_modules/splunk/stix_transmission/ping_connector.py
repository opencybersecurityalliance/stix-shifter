from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
import json
from stix_shifter_utils.utils.error_response import ErrorResponder

class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]
    
    def ping_connection(self):
        response = self.api_client.ping_box()
        response_code = response.code

        response_dict = json.loads(response.read())
        
        return_obj = dict()

        if len(response_dict) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages',0,'text'], connector=self.connector)
        return return_obj
