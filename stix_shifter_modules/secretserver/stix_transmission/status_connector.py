from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from enum import Enum
import json
from stix_shifter_utils.utils.error_response import ErrorResponder

class SecretServerStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'
#  It is a synchronous connector , so pass the status check

class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def __getStatus(self, status):
        return
    def create_status_connection(self, search_id):
        pass
