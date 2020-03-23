from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.qradar_ping import QRadarPing
from .stix_transmission.qradar_query_connector import QRadarQueryConnector
from .stix_transmission.qradar_status_connector import QRadarStatusConnector
from .stix_transmission.qradar_delete_connector import QRadarDeleteConnector
from .stix_transmission.qradar_results_connector import QRadarResultsConnector
from .stix_transmission.arielapiclient import APIClient

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super(EntryPoint, self).__init__(options)
        
        if connection:
            api_client = APIClient(connection, configuration)
            results_connector = QRadarResultsConnector(api_client)
            status_connector = QRadarStatusConnector(api_client)
            delete_connector = QRadarDeleteConnector(api_client)
            query_connector = QRadarQueryConnector(api_client)
            ping_connector = QRadarPing(api_client)
            
            self.set_results_connector(results_connector)
            self.set_status_connector(status_connector)
            self.set_delete_connector(delete_connector)
            self.set_query_connector(query_connector)
            self.set_ping_connector(ping_connector)
        else:
            self.setup_translation_simple('events')