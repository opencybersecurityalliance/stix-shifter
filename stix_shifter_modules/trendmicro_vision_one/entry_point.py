from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint

from .stix_transmission.api_client import APIClient
from .stix_transmission.delete_connector import DeleteConnector
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.status_connector import StatusConnector


class EntryPoint(BaseEntryPoint):
    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            api_client = APIClient(connection, configuration)
            ping_connector = PingConnector(api_client)
            query_connector = QueryConnector(api_client)
            status_connector = StatusConnector()
            results_connector = ResultsConnector(api_client)
            delete_connector = DeleteConnector(api_client)

            self.set_results_connector(results_connector)
            self.set_status_connector(status_connector)
            self.set_delete_connector(delete_connector)
            self.set_query_connector(query_connector)
            self.set_ping_connector(ping_connector)

        self.setup_translation_simple(dialect_default="endpointActivityData")
