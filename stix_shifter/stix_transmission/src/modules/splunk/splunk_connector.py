from ..base.base_connector import BaseConnector
from .splunk_query_connector import SplunkQueryConnector
from .splunk_status_connector import SplunkStatusConnector
from .splunk_results_connector import SplunkResultsConnector
from .splunk_delete_connector import SplunkDeleteConnector
from .spl_api_client import APIClient
from .splunk_ping import SplunkPing
from .splunk_auth import SplunkAuth

import json


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.delete_connector = SplunkDeleteConnector(self.api_client)
        self.results_connector = SplunkResultsConnector(self.api_client)
        self.status_connector = SplunkStatusConnector(self.api_client)
        self.query_connector = SplunkQueryConnector(self.api_client)
        self.ping_connector = SplunkPing(self.api_client)
        self.is_async = True
