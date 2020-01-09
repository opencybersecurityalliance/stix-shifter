from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
from enum import Enum
import json
from .....utils.error_response import ErrorResponder

class CloudIdentityStatus(Enum):
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class CloudIdentityStatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_status_connection(self, status):
        switcher = {
            CloudIdentityStatus.WAIT.value: Status.RUNNING,
            CloudIdentityStatus.EXECUTE.value: Status.RUNNING,
            CloudIdentityStatus.SORTING.value: Status.RUNNING,
            CloudIdentityStatus.COMPLETED.value: Status.COMPLETED,
            CloudIdentityStatus.CANCELED.value: Status.CANCELED,
            CloudIdentityStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(status).value    
    