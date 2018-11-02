from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
from enum import Enum
import json


class QRadarStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class QRadarStatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def __getStatus(self, qradar_status):
        switcher = {
            QRadarStatus.WAIT.value: Status.RUNNING,
            QRadarStatus.EXECUTE.value: Status.RUNNING,
            QRadarStatus.SORTING.value: Status.RUNNING,
            QRadarStatus.COMPLETED.value: Status.COMPLETED,
            QRadarStatus.CANCELED.value: Status.CANCELED,
            QRadarStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(qradar_status).value

    def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search(search_id)
            response_code = response.code
            response_json = json.loads(response.read())

            # Construct a response object
            return_obj = dict()

            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = self.__getStatus(response_json['status'])
                return_obj['progress'] = response_json['progress']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when getting search status: {}'.format(err))
            raise
