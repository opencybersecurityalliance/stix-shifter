from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector

class AsyncDummyDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        try:
            response = self.api_client.delete_search(search_id)
            return response
        except Exception as err:
            print('error when deleting search {}:'.format(err))
            raise
