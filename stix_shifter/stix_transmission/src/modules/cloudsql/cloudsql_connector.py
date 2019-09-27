from ..base.base_connector import BaseConnector
from .cloudsql_ping import CloudSQLPing
from .cloudsql_query_connector import CloudSQLQueryConnector
from .cloudsql_status_connector import CloudSQLStatusConnector
from .cloudsql_results_connector import CloudSQLResultsConnector
from .cloudsql_delete_connector import CloudSQLDeleteConnector
from ibmcloudsql import SQLQuery

import json


class Connector(BaseConnector):
    # TODO: config params passed into constructor instance
    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        client_info = configuration.get('client_info')
        instance_crn = connection.get('instance_crn')
        target_cos = connection.get('target_cos')

        self.api_client = SQLQuery(auth["bxapikey"], instance_crn, target_cos,
                                   client_info=client_info)
        self.api_client.logon()
        self.results_connector = CloudSQLResultsConnector(self.api_client)
        self.status_connector = CloudSQLStatusConnector(self.api_client)
        self.query_connector = CloudSQLQueryConnector(self.api_client)
        self.ping_connector = CloudSQLPing(self.api_client)
        self.delete_connector = CloudSQLDeleteConnector(self.api_client)
        self.is_async = True
