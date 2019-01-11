from ..base.base_delete_connector import BaseDeleteConnector
import json


class QRadarDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        try:
            response = self.api_client.delete_search(search_id)
            response_code = response.code
            response_json = json.loads(response.read())
            # Construct a response object
            return_obj = dict()
            if response_code == 202:
                return_obj['success'] = True
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']

            return return_obj
        except Exception as err:
            print('error when deleting search {}:'.format(err))
            raise
