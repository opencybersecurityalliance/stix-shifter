from ..base.base_connector import BaseConnector
from .carbonblack_ping import CarbonBlackPing
from .carbonblack_api_client import APIClient


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.ping_connector = CarbonBlackPing(self.api_client)
        self.is_async = False
