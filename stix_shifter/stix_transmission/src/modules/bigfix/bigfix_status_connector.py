from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
import math
import json
import re
import sys
from .....utils.error_response import ErrorResponder
import xmltodict

class UnexpectedResponseException(Exception):
    pass

class BigFixStatusConnector(BaseStatusConnector):

    RELEVANCE = 'number of bes computers whose (last report time of it > (now - 60 * minute))'
    PATTERN = '<Answer type="integer">(.*)</Answer>'
    DEFAULT_CLIENT_COUNT = sys.maxsize

    def __init__(self, api_client):
        self.api_client = api_client

    def get_succes_status(self, data_dict):
        items = ErrorResponder.get_struct_item(data_dict, ['results','+isFailure=False'])
        return len(items) > 0

    def create_status_connection(self, search_id):
        response_txt = None
        return_obj = dict()
        
        try:
            response = self.api_client.get_sync_query_results(self.RELEVANCE)
            response_txt = response.read().decode('utf-8')
            client_count = self.DEFAULT_CLIENT_COUNT
            search = re.search(self.PATTERN, response_txt, re.IGNORECASE)

            if search:
                client_count = search.group(1)

            client_count = int(client_count)

            response_txt = None
            response = self.api_client.get_search_results(search_id, '0', '1')
            response_code = response.code
            response_txt = response.read().decode('utf-8')
            
            if 199 < response_code < 300:
                try:
                    response_dict = json.loads(response_txt)
                    return_obj['success'] = True
                    return_obj['status'] = Status.RUNNING.value

                    reporting_agents = int(response_dict.get('reportingAgents', '0'))
                    total_results = int(response_dict.get('totalResults', '0'))

                    if self.DEFAULT_CLIENT_COUNT == client_count:
                        return_obj['progress'] = 0
                    else:
                        progress = (reporting_agents / client_count) * 100
                        progress_floor = math.floor(progress)
                        return_obj['progress'] = progress_floor

                    if client_count <= reporting_agents:
                        return_obj['status'] = Status.COMPLETED.value
                        if total_results <= 0:
                            return_obj['status'] = Status.ERROR.value

                    if return_obj['success'] == True and return_obj['status'] == Status.COMPLETED.value:
                        if not self.get_succes_status(response_dict):
                            return_obj['status'] = Status.ERROR.value
                            ErrorResponder.fill_error(return_obj, response_dict, ['results', '+isFailure=True','~result'])

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
            else :
                raise e

        return return_obj

