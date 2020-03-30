from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector

class AsyncDummyQueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_query_connection(self, query):
        try:
            response = self.api_client.create_search(query)
            return response
        except Exception as err:
            print('error when creating search: {}'.format(err))
            raise
