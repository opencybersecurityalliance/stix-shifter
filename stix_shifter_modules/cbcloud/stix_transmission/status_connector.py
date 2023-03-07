import json

from enum import Enum
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class CbCloudStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    # Map data source status to connector status
    def __getStatus(self, status):
        switcher = {
            CbCloudStatus.RUNNING.value: Status.RUNNING,
            CbCloudStatus.COMPLETED.value: Status.COMPLETED,
            CbCloudStatus.CANCELED.value: Status.CANCELED,
            CbCloudStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(status).value

    async def create_status_connection(self, search_id):
        response = await self.api_client.get_search_status(search_id)
        response_code = response.code
        response_text = response.read()
        error = None
        response_dict = dict()

        try:
            response_dict = json.loads(response_text)
        except ValueError as ex:
            self.logger.debug(response_text)
            error = Exception(f'Can not parse response: {ex}')

        # Based on the response
        # return_obj['success'] = True or False
        # return_obj['status'] = One of the statuses as defined in the Status class:
        # Status.RUNNING, Status.COMPLETED, Status.CANCELED, Status.ERROR
        # return_obj['progress'] = Some progress code if returned from the API

        # Construct a response object
        return_obj = dict()
        return_obj['success'] = False

        if response_dict and response_code == 200:
            completed = response_dict['completed']
            contacted = response_dict['contacted']
            return_obj['success'] = True
            return_obj['progress'] = completed
            return_obj['contacted'] = contacted

            # Not all searchers have returned their results
            if completed < contacted:
                return_obj['status'] = self.__getStatus('RUNNING')
            # Search has completed
            else:
                return_obj['status'] = self.__getStatus('COMPLETED')
                return_obj['progress'] = 100
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=error, connector=self.connector)

        return return_obj
