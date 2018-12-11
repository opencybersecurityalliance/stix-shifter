from ..base.base_query_connector import BaseQueryConnector
import json


class QRadarQueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.create_search(query)
            response_code = response.code
            response_json = json.loads(response.read())

            # Construct a response object
            return_obj = dict()

            if response_code == 201:
                return_obj['success'] = True
                return_obj['search_id'] = response_json['search_id']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when creating search: {}'.format(err))
            raise
