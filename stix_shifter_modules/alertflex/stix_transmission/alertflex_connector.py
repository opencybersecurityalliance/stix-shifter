from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from .api_client import APIClient
import json


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)

    def _handle_errors(self, response, return_obj):
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            if response_txt:
                response_json = json.loads(response_txt)
                if 'results' in response_json:
                    return_obj['data'] = response_json['results']
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'])
        else:
            raise UnexpectedResponseException
        return return_obj

    def ping_connection(self):
        response_txt = None
        return_obj = {}
        try:
            response = self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e

    # Query is sent to data source and results are returned in one step
    def create_query_connection(self, query):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.run_search(query)
        response_code = response.code
        response_dict = json.loads(response.read())

        # Construct a response object
        return_obj = dict()

        if 200 <= response_code < 202:
            return_obj['success'] = True
            return_obj['search_id'] = response_dict
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'])
        return return_obj

    def create_results_connection(self, search_id, offset, length):
        return_obj = {}
        try:
            return_obj['success'] = True
            return_obj['data'] = search_id
            return return_obj

        except Exception as e:
            raise e
