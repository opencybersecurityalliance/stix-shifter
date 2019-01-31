from ..base.base_ping import BasePing
import json
from .....utils.error_response import ErrorResponder

class SplunkPing(BasePing):
    def __init__(self, api_client):
        self.api_client = api_client
    
    def ping(self):
        response = self.api_client.ping_box()
        response_code = response.code

        response_dict = json.loads(response.read())
        
        return_obj = dict()

        if len(response_dict) > 0 and response_code == 200:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages',0,'text'])
        return return_obj
