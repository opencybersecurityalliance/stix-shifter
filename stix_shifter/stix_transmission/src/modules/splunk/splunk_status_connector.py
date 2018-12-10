from ..base.base_status_connector import BaseStatusConnector, Status
from .spl_api_client import APIClient
import json
import math


class SplunkStatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search(search_id)
            response_code = response.code
            response_json = json.load(response)
            
            status, progress = '', ''
            
            if 'entry' in response_json and isinstance(response_json['entry'], list):
                content = response_json['entry'][0]['content']
                progress = math.ceil(content['doneProgress'] * 100)  # convert 0-1.0 scale to <int>0-100

                if content['isDone'] is True:
                    status = Status.COMPLETED.value
                elif content['isFailed'] is True:
                    status = Status.ERROR.value
                elif content['isFinalized'] is True:
                    status = Status.CANCELED.value
                elif progress < 100:
                    status = Status.RUNNING.value
                else:
                    status = 'NA'
            
            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = status
                return_obj['progress'] = progress
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['messages'][0]['text']

            return return_obj
        except Exception as err:
            print('error when getting search status: {}'.format(err))
            raise
