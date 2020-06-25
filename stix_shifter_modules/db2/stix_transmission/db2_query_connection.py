from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json


class DB2QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        # send the query with connected api client.
        response = self.api_client.get_query(query)
        return_obj = dict()
        code = response["code"]
        # the api_client.get_query response object looks like
        # For Synchronous calls query does not execute, it just returns the object below
        # {"code": <code>, search_id: <search_id>}
        # build it out and return it
        if code == 200:
            return_obj['success'] = True
            return_obj['search_id'] = response['search_id']
            return return_obj
        ErrorResponder.fill_error(return_obj, response, ['message'])
        return return_obj
