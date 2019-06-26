from ..base.base_connector import BaseConnector
from .carbonblack_api_client import APIClient
import json
from .....utils.error_response import ErrorResponder

class UnexpectedResponseException(Exception):
    pass

class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.ping_connector = self
        self.results_connector = self
        self.status_connector = self
        self.query_connector = self
        self.is_async = False

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

    def ping(self):
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

    def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}

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
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
