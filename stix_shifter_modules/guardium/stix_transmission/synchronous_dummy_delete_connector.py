from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.utils.error_response import ErrorResponder

class SynchronousDummyDeleteConnector(BaseDeleteConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def delete_query_connection(self, search_id):
        try:
            response_dict = self.api_client.delete_search(search_id)
            response_code = response_dict["code"]

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = response_code['success']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            return response
        except Exception as err:
            print('error when deleting search {}:'.format(err))
            raise
