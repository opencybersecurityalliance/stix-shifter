from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector

class AsyncDummyResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response = self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response["code"]

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response['data']
            else:
                return_obj['success'] = False
                return_obj['error'] = response['message']
            return return_obj
        except Exception as err:
            print('error when getting search results: {}'.format(err))
            raise
