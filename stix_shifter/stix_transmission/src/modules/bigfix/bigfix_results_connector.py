from ..base.base_results_connector import BaseResultsConnector
import json
from .....utils.error_response import ErrorResponder
import xmltodict

class UnexpectedResponseException(Exception):
    pass

class BigFixResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_success_status(self, data_dict):
        items = ErrorResponder.get_struct_item(data_dict, ['results','+isFailure=False'])
        return len(items) > 0

    def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = dict()
        try:
            response = self.api_client.get_search_results(search_id, offset, length)
            response_txt = response.read().decode('utf-8')
            response_code = response.code
            
            if 199 < response_code < 300:
                try:
                    response_dict = json.loads(response_txt)
                    return_obj['success'] = self.get_success_status(response_dict)
                    return_obj['data'] = response_dict['results']
                except json.decoder.JSONDecodeError:
                    response_dict = xmltodict.parse(response_txt)
                    ErrorResponder.fill_error(return_obj, response_dict, ['BESAPI','ClientQueryResults','QueryResult', '+IsFailure=1','~Result'])
            else:
                if ErrorResponder.is_plain_string(response_txt):
                    ErrorResponder.fill_error(return_obj, message=response_txt)
                else:
                    raise UnexpectedResponseException
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
        return return_obj
