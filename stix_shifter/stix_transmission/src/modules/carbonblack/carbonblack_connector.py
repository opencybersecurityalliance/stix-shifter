from ..base.base_connector import BaseConnector
from .carbonblack_api_client import APIClient
import json


class Connector(BaseConnector):
    def __init__(self, connection, configuration, dialect="process"):
        if dialect not in ["process", "binary"]:
            raise NotImplementedError # TODO what's the best exception type to raise?

        self.api_client = APIClient(connection, configuration, dialect=dialect)
        self.ping_connector = self
        self.results_connector = self
        self.query_connector = self
        self.is_async = False

    def ping(self):
        try:
            response = self.api_client.ping_box()
            response_code = response.code
            response_json = json.loads(response.read())

            return_obj = dict()

            if len(response_json) > 0 and 200 <= response_code < 300:
                return_obj['success'] = True
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when pinging data source'
            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when pinging data source: {}'.format(err)
            return return_obj

    def create_query_connection(self, query):
        return {"success": True, "search_id": query}

    def create_results_connection(self, search_id, offset, length):
        try:
            query = search_id
            response = self.api_client.run_search(query)
            response_code = response.code
            response_json = json.loads(response.read())
            return_obj = dict()

            print(response_json)
            if 200 <= response_code < 300 and 'results' in response_json:
                return_obj['success'] = True
                return_obj['data'] = response_json['results']
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when creating search'

            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when creating search: {}'.format(err)
            return return_obj

