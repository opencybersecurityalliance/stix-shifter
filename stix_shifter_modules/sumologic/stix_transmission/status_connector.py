from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class StatusSumologic(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'FORCE PAUSED'
    EXECUTE = 'GATHERING RESULTS'
    SORTING = 'SORTING'
    COMPLETED = 'DONE GATHERING RESULTS'
    CANCELED = 'CANCELLED'
    ERROR = 'ERROR'


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    # Map data source status to connector status
    def __getStatus(self, status):
        switcher = {
            StatusSumologic.WAIT.value: Status.RUNNING,
            StatusSumologic.EXECUTE.value: Status.RUNNING,
            StatusSumologic.SORTING.value: Status.RUNNING,
            StatusSumologic.COMPLETED.value: Status.COMPLETED,
            StatusSumologic.CANCELED.value: Status.CANCELED,
            StatusSumologic.ERROR.value: Status.ERROR
        }
        return switcher.get(status).value

    def create_status_connection(self, search_id):
        try:
            response_dict = self.api_client.get_search_status(search_id)
            # Based on the response
            # return_obj['success'] = True or False
            # return_obj['status'] = One of the statuses as defined in the Status class:
            # Status.RUNNING, Status.COMPLETED, Status.CANCELED, Status.ERROR
            # return_obj['progress'] = Some progress code if returned from the API
            # Construct a response object
            response_code = response_dict.code
            return_obj = dict()

            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = self.__getStatus(response_dict.object)
                return_obj['progress'] = 100
            else:
                return_obj['success'] = False
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search status: {}'.format(err))
            raise
