from ..base.base_delete_connector import BaseDeleteConnector
import json


class SplunkDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client
    
    def delete_query_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.delete_search(search_id)
            response_code = response.code
            response_json = json.load(response) 

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
            else:
                # extract message
                if len(response_json['messages']) > 0:
                    message = response_json['messages'][0]['text'] 
                else:
                    message = "Unknown sid."

                return_obj['success'] = False
                return_obj['error'] = message

            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when deleting search id {} message: {}'.format(search_id, err)
            return return_obj
