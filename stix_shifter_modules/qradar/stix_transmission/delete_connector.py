from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
import json


class DeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        response = self.api_client.delete_search(search_id)
        response_code = response.code
        response_json = json.loads(response.read())
        # Construct a response object
        return_obj = dict()
        if response_code == 202:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_json, ['message'])

        return return_obj