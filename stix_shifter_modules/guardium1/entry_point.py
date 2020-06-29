from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.guardiumapiclient import APIClient
from .stix_transmission.guardium_ping_connector import GuardiumPingConnector
from .stix_transmission.guardium_query_connector import GuardiumQueryConnector
from .stix_transmission.guardium_status_connector import GuardiumStatusConnector
from .stix_transmission.guardium_results_connector import GuardiumResultsConnector
from .stix_transmission.guardium_delete_connector import GuardiumDeleteConnector

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)
        #TODO add test cases

        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = GuardiumPingConnector(api_client)
            query_connector = GuardiumQueryConnector(api_client)
            status_connector = GuardiumStatusConnector(api_client)
            delete_connector = GuardiumDeleteConnector(api_client)
            results_connector = GuardiumResultsConnector(api_client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
        else:
            self.setup_translation_simple('default')