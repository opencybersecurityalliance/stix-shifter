from ..base.base_query_connector import BaseQueryConnector
import re


class BigFixQueryConnector(BaseQueryConnector):

    PATTERN = '<ID>(.*)</ID>'
    DEFAULT_ID = 'UNKNOWN'

    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        try:
            response = self.api_client.create_search(query)
            response_code = response.code
            result = response.read().decode('utf-8')
            search_id = self.DEFAULT_ID
            search = re.search(self.PATTERN, result, re.IGNORECASE)

            if search:
                search_id = search.group(1)

            return_obj = dict()

            if 199 < response_code < 300:
                return_obj['success'] = True
                return_obj['search_id'] = search_id
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when creating search'

            if search_id == self.DEFAULT_ID:
                return_obj['success'] = False
                return_obj['error'] = 'error when creating search'
            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when creating search: {}'.format(err)
            return return_obj
