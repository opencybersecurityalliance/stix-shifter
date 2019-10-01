from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
from enum import Enum
import json
from .....utils.error_response import ErrorResponder

class CloudIdentityStatusConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_status_connector(self, search_id):
        

    