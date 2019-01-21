from ..base.base_connector import BaseConnector
from .carbonblack_ping import CarbonBlackPing
from .carbonblack_results_connector import CarbonBlackResultsConnector
from .carbonblack_query_connector import CarbonBlackQueryConnector
from .carbonblack_api_client import APIClient


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.ping_connector = CarbonBlackPing(self.api_client)
        self.results_connector = CarbonBlackResultsConnector(self.api_client)
        self.query_connector = CarbonBlackQueryConnector()
        self.is_async = False
