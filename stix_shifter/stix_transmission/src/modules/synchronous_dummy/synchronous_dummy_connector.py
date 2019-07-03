from ..base.base_connector import BaseConnector
from .....utils.error_response import ErrorResponder
from .api_client import APIClient
import json


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.is_async = False
        self.ping_connector = self
        self.results_connector = self
        self.status_connector = self
        self.query_connector = self

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

    def ping(self):
        return_obj = {}
        try:
            response = self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as err:
            print('error when pinging datasource {}:'.format(err))
            raise

    # Leave dummy implementation as is for synchronous data sources
    def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    # Leave dummy implementation as is for synchronous data sources
    def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}

    # Query is sent to data source and results are returned in one step
    def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = {}
        try:
            query = search_id
            response = self.api_client.run_search(query, offset, length)
            return self._handle_errors(response, return_obj)

        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
