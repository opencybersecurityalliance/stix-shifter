from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    def create_query_connection(self, query):
        """
        Function to create query connection
        :param query: str, Query
        :return: dict
        """
        try:
            return_obj = self.api_client.create_search(query)
        except Exception as err:
            return_obj = dict()
            response_error = err
            ErrorResponder.fill_error(return_obj, response_error, ['message'], connector=self.connector)
        return return_obj
