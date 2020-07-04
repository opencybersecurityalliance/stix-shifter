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
        response_code = response['code']

        if 200 <= response_code < 300:
            return_obj['success'] = True
            response_json = response
            if 'results' in response_json:
                return_obj['data'] = response_json['results']
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
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = {}
        try:
            response = self.api_client.run_search(search_id, offset, length)
            response_code = response.code
            response_dict = json.loads(response.read())

            # Construct a response object
            return_obj = dict()

            if 200 <= response_code < 300:
                return_obj['success'] = True
                return_obj['data'] = response_dict
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['messages', 0, 'text'])
            return return_obj

        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
