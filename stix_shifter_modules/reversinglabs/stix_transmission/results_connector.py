from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json

class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    async def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # print(search_id, min_range, max_range, length)
            search_id = search_id.replace('\'', "\"")
            query_json= json.loads(search_id)
            response = await self.api_client.get_search_results(query_json)
            response_code = response['code']

            # Grab the response, extract the response code, and convert it to readable json
            # response_dict = self.api_client.get_search_results(search_id, min_range, max_range)
            # json_data = json.loads(response.read().decode('utf-8'))
            # print(type(response), response)
            # response_code = response.code
            json_data = response['message']

            if "rl" in json_data.keys():
                json_data['rl'] = [json_data['rl']]
            else:
                rl_data = {}
                rl_data['rl'] = [{'message': 'IOC not found'}]
                json_data = rl_data

            # # Construct a response object
            return_obj = dict()
            if response_code == 200:
                json_data['data'] = query_json['data']
                json_data['dataType'] = query_json['dataType']
                return_obj['success'] = True
                return_obj['data'] = [json_data]
            else:
                json_data['data'] = query_json['data']
                json_data['dataType'] = query_json['dataType']
                json_data['namespace'] = response['namespace']
                return_obj['success'] = True
                return_obj['data'] = [json_data]

                ErrorResponder.fill_error(return_obj, response, ['message'], connector='reversinglabs')

            # else:
            #     # ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            #     ErrorResponder.fill_error(return_obj, json_data)
            #     return_obj['error'] = json_data['error']
            return return_obj
        except Exception as err:
            response['message'] = str(err)
            self.logger.error('error when getting search results: {}'.format(err))
            ErrorResponder.fill_error(return_obj, response, ['message'], connector='reversinglabs')
            raise
