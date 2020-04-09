from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.bigfix_api_client import APIClient
from .stix_transmission.bigfix_ping_connector import BigFixPingConnector
from .stix_transmission.bigfix_query_connector import BigFixQueryConnector
from .stix_transmission.bigfix_status_connector import BigFixStatusConnector
from .stix_transmission.bigfix_results_connector import BigFixResultsConnector
from .stix_transmission.bigfix_delete_connector import BigFixDeleteConnector


class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        
        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = BigFixPingConnector(api_client)
            query_connector = BigFixQueryConnector(api_client)
            status_connector = BigFixStatusConnector(api_client)
            results_connector = BigFixResultsConnector(api_client)
            delete_connector = BigFixDeleteConnector(api_client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            self.setup_translation_simple('default')