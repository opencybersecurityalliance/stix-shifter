from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector, Status
import math
import json
import re
import sys
import time
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import xmltodict

PROGRESS_THRESHOLD = 50


class UnexpectedResponseException(Exception):
    pass


class StatusConnector(BaseStatusConnector):

    RELEVANCE = 'number of bes computers whose (last report time of it > (now - 60 * minute))'
    PATTERN = '<Answer type="integer">(.*)</Answer>'
    DEFAULT_CLIENT_COUNT = sys.maxsize

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def _get_progress_status(self, client_count, reporting_agents, return_obj):
        """
        Returns the progress based on API query result(reporting_agents) and Bes computers
        health checked in within last 1 hour(client_count)
        :param client_count: int
        :param reporting_agents: int
        :param return_obj: dict
        :return: dict
        """
        if self.DEFAULT_CLIENT_COUNT == client_count:
            return_obj['progress'] = 0
        else:
            progress = (reporting_agents / client_count) * 100
            progress_floor = math.floor(progress)
            return_obj['progress'] = progress_floor
        return return_obj

    def update_query_status(self, return_obj, response_dict, client_count):
        """
        Updates the status of query based on progress by comparing against PROGRESS_THRESHOLD
        if progress < PROGRESS_THRESHOLD ==> STATUS == RUNNING
        if progress > PROGRESS_THRESHOLD     ==> wait for a relative small period based on proximity of progress to 100%
        then changes STATUS == COMPLETED
        :param return_obj: dict
        :param response_dict: dict
        :param client_count: int
        :return: dict
        """
        reporting_agents = int(response_dict.get('reportingAgents', '0'))
        return_obj = self._get_progress_status(client_count, reporting_agents, return_obj)
        if client_count <= reporting_agents:
            return_obj['status'] = Status.COMPLETED.value
            return_obj['progress'] = 100
        else:
            if return_obj['progress'] > PROGRESS_THRESHOLD:
                return_obj['status'] = Status.COMPLETED.value
                return_obj['progress'] = 100
        return return_obj

    def status_api_response(self, search_id, client_count):
        """
        Sub-method of create_status_connection for returning status
        dictionary object for a given query ID
        :param search_id: int
        :param client_count: int
        :return: dict
        """
        return_obj = dict()
        try:
            response = self.api_client.get_search_results(search_id, '0', '1')
            response_code = response.code
            response_txt = response.read().decode('utf-8')

            if 199 < response_code < 300:
                try:
                    response_dict = json.loads(response_txt)
                    return_obj['success'] = True
                    return_obj['status'] = Status.RUNNING.value
                    return_obj = self.update_query_status(return_obj, response_dict, client_count)
                except json.decoder.JSONDecodeError:
                    response_dict = xmltodict.parse(response_txt)
                    ErrorResponder.fill_error(return_obj, response_dict, ['BESAPI', 'ClientQueryResults',
                                                                          'QueryResult', '+IsFailure=1', '~Result'], connector=self.connector)
            else:
                if ErrorResponder.is_plain_string(response_txt):
                    ErrorResponder.fill_error(return_obj, message=response_txt)
                else:
                    raise UnexpectedResponseException
        except Exception as e:
            if e.__class__.__name__ in ['ConnectionError', 'ProxyError']:
                ErrorResponder.fill_error(return_obj, message='API call disconnected/interrupted', connector=self.connector)
                return_obj['status'] = Status.ERROR.value
            else:
                raise e

        return return_obj

    def create_status_connection(self, search_id):
        """
        Return status dictionary object for given query ID
        :param search_id: int
        :return: dict
        """
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
        except Exception as e:
            if e.__class__.__name__ in ['ConnectionError', 'ProxyError']:
                ErrorResponder.fill_error(return_obj, message='API call disconnected/interrupted', connector=self.connector)
                return_obj['status'] = Status.ERROR.value
            elif response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
        return return_obj
