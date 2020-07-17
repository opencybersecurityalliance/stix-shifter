from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class UnexpectedResponseException(Exception):
    pass

class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)

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
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = {}
        try:
            search_id = json.loads(search_id)
            query = search_id["query"]
            dialect = search_id["dialect"]
            response = self.api_client.run_search(query, dialect, start=offset, rows=length)
            return self._handle_errors(response, return_obj)

        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
