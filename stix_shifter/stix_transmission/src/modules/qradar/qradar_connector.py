from ..base.base_connector import BaseConnector
from .qradar_ping import QRadarPing
from .qradar_query_connector import QRadarQueryConnector
from .qradar_status_connector import QRadarStatusConnector
from .qradar_delete_connector import QRadarDeleteConnector
from .qradar_results_connector import QRadarResultsConnector
from .arielapiclient import APIClient


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.results_connector = QRadarResultsConnector(self.api_client)
        self.status_connector = QRadarStatusConnector(self.api_client)
        self.delete_connector = QRadarDeleteConnector(self.api_client)
        self.query_connector = QRadarQueryConnector(self.api_client)
        self.ping_connector = QRadarPing(self.api_client)
        self.is_async = True
