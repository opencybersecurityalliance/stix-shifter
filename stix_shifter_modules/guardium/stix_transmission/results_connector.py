from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = int(offset) + int(length)
            # Grab the response, extract the response code, and convert it to readable json
            response = await self.api_client.get_search_results(search_id, min_range, max_range)
            response_code = response.code

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                if hasattr(response,'content'):
                    data= json.loads(response.content)
                else:    
                    data = json.loads(response.read())
                #print("+++++++++++++++++data ="+json.dumps(data))    
                if type(data) == dict and 'ID' in data.keys() and 'Message' in data.keys() and data['ID'] == 0 and\
                        'The Query did not retrieve any records' == data['Message']:
                    data = []
                return_obj['data'] = data
            else:
                ErrorResponder.fill_error(return_obj, response, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            raise
