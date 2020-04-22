from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.api_client import APIClient
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.status_connector import StatusConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.delete_connector import DeleteConnector
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

import os

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        
        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = PingConnector(api_client)
            query_connector = QueryConnector(api_client)
            status_connector = StatusConnector(api_client)
            results_connector = ResultsConnector(api_client)
            delete_connector = DeleteConnector(api_client)
            
            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            self.setup_translation_simple('flows')