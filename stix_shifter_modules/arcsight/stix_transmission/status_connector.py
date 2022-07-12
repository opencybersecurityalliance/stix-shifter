import json
import math
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
from stix_shifter_utils.utils.error_response import ErrorResponder

DEFAULT_LIMIT = 10000


class ArcsightStatus(Enum):
    # STARTING, RUNNING, TIMEOUT, COMPLETE, STOP. ERROR
    STARTING = 'starting'
    RUNNING = 'running'
    TIMEOUT = 'timeout'
    COMPLETE = 'complete'
    STOP = 'stop'
    ERROR = 'error'


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    # Map data source status to connector status
    @staticmethod
    def __getStatus(arcsight_status):
        """
        Return the status of the search id
        :param arcsight_status: str, status
        :return: str
        """
        switcher = {
            ArcsightStatus.STARTING.value: Status.RUNNING,
            ArcsightStatus.RUNNING.value: Status.RUNNING,
            ArcsightStatus.TIMEOUT.value: Status.TIMEOUT,
            ArcsightStatus.COMPLETE.value: Status.COMPLETED,
            ArcsightStatus.STOP.value: Status.CANCELED,
            ArcsightStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(arcsight_status).value

    def create_status_connection(self, search_id):
        """
        Fetching the progress and the status of the search id
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        limit = DEFAULT_LIMIT
        user_limit = None
        try:
            search_id_length = len(search_id.split(':'))
            search_id_values = search_id.split(':')
            if search_id_length == 2:
                search_session_id, user_session_id = search_id_values
            elif search_id_length == 3:
                search_session_id, user_session_id, user_limit = search_id_values
            else:
                raise SyntaxError("Invalid search_id format : " + str(search_id))

            if user_limit and int(user_limit) <= DEFAULT_LIMIT:
                limit = user_limit
            response = self.api_client.get_search_status(search_session_id, user_session_id)
            raw_response = response.read()
            response_code = response.code
            self.status_progress(return_obj, response_code, raw_response, limit)

        except Exception as err:
            response_error = err
            ErrorResponder.fill_error(return_obj, response_error, ['message'], connector=self.connector)

        return return_obj

    def status_progress(self, return_obj, response_code, raw_response, limit):
        """
        status progress calculation
        :param return_obj: dict, building return response dict
        :param raw_response: str, Api response,
        :param response_code: int, Api call response code
        :param limit: int, limit for status calculation """
        if 199 < response_code < 300:
            response_dict = json.loads(raw_response)
            return_obj['success'] = True
            return_obj['status'] = self.__getStatus(response_dict['status'])
            results = int(response_dict['hit'])
            if return_obj['status'] == 'COMPLETED':
                return_obj['progress'] = 100
            elif return_obj['status'] == 'RUNNING':
                progress = (results / int(limit)) * 100
                progress_floor = math.floor(progress)
                return_obj['progress'] = progress_floor
                if return_obj['progress'] >= 100:
                    return_obj['progress'] = 100
                    return_obj['status'] = 'COMPLETED'
            else:
                return_obj['progress'] = 0
        # arcsight logger error codes - currently unavailable state
        elif response_code in [500, 503]:
            response_string = raw_response.decode()
            ErrorResponder.fill_error(return_obj, response_string, ['message'], connector=self.connector)
        elif isinstance(json.loads(raw_response), dict):
            response_error = json.loads(raw_response)
            response_dict = response_error['errors'][0]
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        else:
            raise Exception(raw_response)
