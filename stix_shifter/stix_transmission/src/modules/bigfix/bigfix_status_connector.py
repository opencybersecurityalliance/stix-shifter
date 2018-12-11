from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
import math
import json
import re
import sys


class BigFixStatusConnector(BaseStatusConnector):

    RELEVANCE = 'number of bes computers whose (last report time of it > (now - 60 * minute))'
    PATTERN = '<Answer type="integer">(.*)</Answer>'
    DEFAULT_CLIENT_COUNT = sys.maxsize

    def __init__(self, api_client):
        self.api_client = api_client

    def create_status_connection(self, search_id):

        try:
            response = self.api_client.get_sync_query_results(self.RELEVANCE)
            result = response.read().decode('utf-8')
            client_count = self.DEFAULT_CLIENT_COUNT
            search = re.search(self.PATTERN, result, re.IGNORECASE)

            if search:
                client_count = search.group(1)

            client_count = int(client_count)

            response = self.api_client.get_search_results(search_id, '0', '1')
            response_code = response.code
            response_json = json.loads(response.read())
            return_obj = dict()

            if 199 < response_code < 300:
                return_obj['success'] = True
                return_obj['status'] = Status.RUNNING.value

                reporting_agents = int(response_json.get('reportingAgents', '0'))
                total_results = int(response_json.get('totalResults', '0'))

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
            else:
                return_obj['success'] = False
                return_obj['error'] = 'error when getting search status'

            return return_obj
        except Exception as err:
            return_obj = dict()
            return_obj['success'] = False
            return_obj['error'] = 'error when getting search status: {}'.format(err)
            return return_obj
