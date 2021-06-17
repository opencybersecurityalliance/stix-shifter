from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_transmission.boto3_client import BOTO3Client
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.status_connector import StatusConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.delete_connector import DeleteConnector


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)

        if connection and configuration:
            boto3_client = BOTO3Client(connection, configuration)
            ping_connector = PingConnector(boto3_client.client)
            query_connector = QueryConnector(boto3_client.client, boto3_client.log_group_names)
            status_connector = StatusConnector(boto3_client.client)
            results_connector = ResultsConnector(boto3_client.client, options)
            delete_connector = DeleteConnector(boto3_client.client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)

        self.setup_translation_simple(dialect_default='guardduty')
