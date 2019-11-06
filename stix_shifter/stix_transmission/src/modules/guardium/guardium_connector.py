from ..base.base_connector import BaseConnector
from .guardium_ping import GuardiumPing
from .guardium_query_connector import GuardiumQueryConnector
from .guardium_status_connector import GuardiumStatusConnector
from .guardium_delete_connector import GuardiumDeleteConnector
from .guardium_results_connector import GuardiumResultsConnector
from .guardiumapiclient import APIClient
import logging

class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.results_connector = GuardiumResultsConnector(self.api_client)
        self.status_connector = GuardiumStatusConnector(self.api_client)
        self.delete_connector = GuardiumDeleteConnector(self.api_client)
        self.query_connector = GuardiumQueryConnector(self.api_client)
        self.ping_connector = GuardiumPing(self.api_client)
        self.is_async = False
        #
        # It is for Guardium
        # Start logging based on logLevel -- for debugging purpuse -- SB
        logFile = "../runlogs/ss_guardium_transmission_run.log"
        logging.basicConfig(filename=logFile, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('\n >>>>>>>>>>> Transmission Run Started. >>>>>>>>>>')
