from ..base.base_status_connector import BaseStatusConnector, Status
from .spl_api_client import APIClient
import json
import math
from enum import Enum
from .....utils.error_response import ErrorResponder

class StatusSplunk(Enum):
    COMPLETED = 'DONE'
    ERROR = 'FAILED'
    RUNNING = 'RUNNING'

class SplunkStatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.get_search(search_id)
        response_code = response.code
        response_dict = json.load(response)
        
        status, progress = '', ''
        
        if 'entry' in response_dict and isinstance(response_dict['entry'], list):
            content = response_dict['entry'][0]['content']
            progress = math.ceil(content['doneProgress'] * 100)  # convert 0-1.0 scale to <int>0-100
            status = content['dispatchState']

            if status == StatusSplunk.COMPLETED.value:
                status = Status.COMPLETED.value
            elif status == StatusSplunk.ERROR.value:
                status = Status.ERROR.value
            else:
                status = Status.RUNNING.value

        # Construct a response object
        return_obj = dict()
        if response_code == 200:
            return_obj['success'] = True
            return_obj['status'] = status
            return_obj['progress'] = progress
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages',0,'text'])
        return return_obj
