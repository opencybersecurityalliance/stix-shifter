from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
import math
import json
import re
import sys
import time
from .....utils.error_response import ErrorResponder
import xmltodict

WAIT_PERIOD = 6


class UnexpectedResponseException(Exception):
    pass


class BigFixStatusConnector(BaseStatusConnector):

    RELEVANCE = 'number of bes computers whose (last report time of it > (now - 60 * minute))'
    PATTERN = '<Answer type="integer">(.*)</Answer>'
    DEFAULT_CLIENT_COUNT = sys.maxsize

    def __init__(self, api_client):
        self.api_client = api_client

    def _get_progress_status(self, client_count, reporting_agents, return_obj):
        if self.DEFAULT_CLIENT_COUNT == client_count:
            return_obj['progress'] = 0
        else:
            progress = (reporting_agents / client_count) * 100
            progress_floor = math.floor(progress)
            return_obj['progress'] = progress_floor
        return return_obj

    def status_api_response(self, search_id, client_count):
        time_iter = self.api_client.client.timeout - WAIT_PERIOD
        return_obj = dict()
        while time_iter > 0:
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
                    return_obj = self._get_progress_status(client_count, reporting_agents, return_obj)
                    if client_count <= reporting_agents:
                        return_obj['status'] = Status.COMPLETED.value
                        if total_results <= 0:
                            return_obj['status'] = Status.ERROR.value
                        break
                    time_iter -= WAIT_PERIOD
                    if time_iter < WAIT_PERIOD:
                        time.sleep(time_iter)
                    else:
                        time.sleep(WAIT_PERIOD)
                except json.decoder.JSONDecodeError:
                    response_dict = xmltodict.parse(response_txt)
                    ErrorResponder.fill_error(return_obj, response_dict, ['BESAPI', 'ClientQueryResults',
                                                                          'QueryResult', '+IsFailure=1', '~Result'])
                    break
            else:
                if ErrorResponder.is_plain_string(response_txt):
                    ErrorResponder.fill_error(return_obj, message=response_txt)
                    break
                else:
                    raise UnexpectedResponseException
        return return_obj

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
            return_obj = self.status_api_response(search_id, client_count)
            if return_obj['progress'] < 100 and return_obj['status'] == Status.RUNNING.value:
                return_obj['status'] = Status.COMPLETED.value
        except Exception as e:
            if e.__class__.__name__ == 'ConnectionError':
                ErrorResponder.fill_error(return_obj, message='API call disconnected/interrupted')
                return_obj['status'] = Status.ERROR.value
            elif response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                print('can not parse response: ' + str(response_txt))
            else:
                raise e
        return return_obj
