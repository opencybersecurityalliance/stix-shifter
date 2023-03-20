
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger as utils_logger
from enum import Enum
import json


class StatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = utils_logger.set_logger(__name__)

    async def create_status_connection(self, search_id):
        return {"success": True, "status": "COMPLETED", "progress": 100}
