from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
import math

DEFAULT_LIMIT = 10000


class AWSCWLOGS(Enum):
    # CANCELLED, COMPLETE, FAILED, RUNNING, SCHEDULED, TIMEOUT, AND UNKNOWN
    CANCELLED = 'Cancelled'
    COMPLETE = 'Complete'
    FAILED = 'Failed'
    RUNNING = 'Running'
    SCHEDULED = 'Scheduled'
    TIMEOUT = 'Timeout'
    UNKNOWN = 'Unknown'


class StatusConnector(BaseStatusConnector):

    def __init__(self, client):
        self.client = client
        self.connector = __name__.split('.')[1]

    @staticmethod
    def _getstatus(awscwlogs_status):
        """
        Return the status of the search id
        :param awscwlogs_status: str,
        :return: str
        """
        switcher = {
            AWSCWLOGS.CANCELLED.value: Status.CANCELED,
            AWSCWLOGS.COMPLETE.value: Status.COMPLETED,
            AWSCWLOGS.FAILED.value: Status.ERROR,
            AWSCWLOGS.RUNNING.value: Status.RUNNING,
            AWSCWLOGS.SCHEDULED.value: Status.RUNNING,
            AWSCWLOGS.TIMEOUT.value: Status.TIMEOUT,
            AWSCWLOGS.UNKNOWN.value: Status.ERROR
        }
        return switcher.get(awscwlogs_status).value

    def create_status_connection(self, search_id):
        """
        Fetching the progress and the status of the search id
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        limit = DEFAULT_LIMIT
        try:
            if ':' in search_id:
                search_id, limit = search_id.split(':')
            query = dict()
            query['queryId'] = search_id
            response_dict = self.client.get_query_results(**query)
            return_obj['success'] = True
            return_obj['status'] = self._getstatus(response_dict['status'])
            results = len(response_dict['results'])
            if return_obj['status'] == 'COMPLETED':
                return_obj['progress'] = 100
            elif return_obj['status'] == 'RUNNING':
                progress = (results / int(limit)) * 100
                progress_floor = math.floor(progress)
                return_obj['progress'] = progress_floor
                if return_obj['progress'] >= 100:
                    return_obj['status'] = 'COMPLETED'
            else:
                return_obj['progress'] = 0
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
