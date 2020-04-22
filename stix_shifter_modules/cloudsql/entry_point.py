from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from ibmcloudsql import SQLQuery
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.status_connector import StatusConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.delete_connector import DeleteConnector

import json

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            auth = configuration.get('auth')
            client_info = configuration.get('client_info')
            instance_crn = connection.get('instance_crn')
            target_cos = connection.get('target_cos')

            api_client = SQLQuery(auth["bxapikey"], instance_crn, target_cos,
                                    client_info=client_info)
            api_client.logon()
            ping_connector = CloudSQLPingConnector(api_client)
            query_connector = CloudSQLQueryConnector(api_client)
            status_connector = CloudSQLStatusConnector(api_client)
            results_connector = CloudSQLResultsConnector(api_client)
            delete_connector = CloudSQLDeleteConnector(api_client)

            self.set_ping_connector(ping_connector)
            self.set_query_connector(query_connector)
            self.set_status_connector(status_connector)
            self.set_results_connector(results_connector)
            self.set_delete_connector(delete_connector)
