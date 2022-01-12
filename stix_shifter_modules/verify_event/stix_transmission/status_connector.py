
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger as utils_logger
from enum import Enum
import json

#TODO Need to check the actual status in verify. This is standard status of any async service
class verifyEventStatus(Enum):
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
        self.logger = utils_logger.set_logger(__name__)

    def __getStatus(self, qradar_status):
        switcher = {
            verifyEventStatus.WAIT.value: Status.RUNNING,
            verifyEventStatus.EXECUTE.value: Status.RUNNING,
            verifyEventStatus.SORTING.value: Status.RUNNING,
            verifyEventStatus.COMPLETED.value: Status.COMPLETED,
            verifyEventStatus.CANCELED.value: Status.CANCELED,
            verifyEventStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(qradar_status).value

    def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        response = self.api_client.get_search(search_id)
        response_code = response.code
        response_text = response.read()

        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
        except Exception as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex} : {response_text}')

        # Construct a response object
        return_obj = dict()

        if response_code == 200:
            return_obj['success'] = True
            return_obj['status'] = self.__getStatus(response_dict['status'])
            return_obj['progress'] = response_dict['progress']
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error)
        return return_obj