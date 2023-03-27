from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
import json
from stix_shifter_utils.utils.error_response import ErrorResponder

class GuardiumStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    def __getStatus(self, status):
        switcher = {
            GuardiumStatus.WAIT.value: Status.RUNNING,
            GuardiumStatus.EXECUTE.value: Status.RUNNING,
            GuardiumStatus.SORTING.value: Status.RUNNING,
            GuardiumStatus.COMPLETED.value: Status.COMPLETED,
            GuardiumStatus.CANCELED.value: Status.CANCELED,
            GuardiumStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(status).value

    async def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        # Verify the input
        response = self.api_client.get_status(search_id)
        response_code = response.status_code
        response_dict = json.loads(response.read())

        # Construct a response object
        return_obj = dict()
        response_code = 200
        if response_code == 200:
            return_obj['success'] = True
            return_obj['status'] = self.__getStatus(response_dict['status'])
            return_obj['progress'] = response_dict.get('progress',"NA")
            return_obj['data'] = response_dict.get('data',"NA")
            return_obj["search_id"] = response_dict.get('search_id',"NA")
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
