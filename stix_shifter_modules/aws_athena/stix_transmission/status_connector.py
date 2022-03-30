from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
import datetime
from dateutil.tz import tzlocal
import math


class AthenaStatus(Enum):
    # QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELLED
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'


class StatusConnector(BaseStatusConnector):

    def __init__(self, client):
        self.client = client
        self.connector = __name__.split('.')[1]

    @staticmethod
    def _getstatus(athena_status):
        """
        Return the status of the search id
        :param athena_status: str,
        :return: str
        """
        switcher = {
            AthenaStatus.QUEUED.value: Status.RUNNING,
            AthenaStatus.RUNNING.value: Status.RUNNING,
            AthenaStatus.SUCCEEDED.value: Status.COMPLETED,
            AthenaStatus.FAILED.value: Status.ERROR,
            AthenaStatus.CANCELLED.value: Status.CANCELED,
        }
        return switcher.get(athena_status).value

    def create_status_connection(self, search_id):
        """
        Fetching the progress and the status of the search id
        :param search_id: str, search id
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            search_id = search_id.split(':')[0]
            if 'dummy' in search_id:
                return_obj = {'success': True, 'status': 'COMPLETED', 'progress': 100}
                return return_obj
            response_dict = self.client.get_query_execution(QueryExecutionId=search_id)
            return_obj['success'] = True
            return_obj['status'] = self._getstatus(response_dict.get('QueryExecution', 'FAILED').
                                                   get('Status', 'FAILED').
                                                   get('State', 'FAILED'))
            if return_obj['status'] == 'COMPLETED':
                return_obj['progress'] = 100
            elif return_obj['status'] == 'RUNNING':
                query_submit_time = response_dict.get('QueryExecution').get('Status').get('SubmissionDateTime')
                if query_submit_time:
                    current_time = datetime.datetime.now(tzlocal())
                    time_delta = current_time - query_submit_time
                    progress = time_delta.total_seconds()
                    progress_floor = math.floor(progress)
                    return_obj['progress'] = progress_floor if progress_floor <= 100 else 99
                else:
                    return_obj['progress'] = 0
            else:
                return_obj['progress'] = 0
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
