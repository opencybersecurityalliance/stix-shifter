from ..base.base_connector import BaseConnector
from .bigfix_ping import BigFixPing
from .bigfix_query_connector import BigFixQueryConnector
from .bigfix_status_connector import BigFixStatusConnector
from .bigfix_delete_connector import BigFixDeleteConnector
from .bigfix_results_connector import BigFixResultsConnector
from .bigfix_api_client import APIClient


class Connector(BaseConnector):
    # TODO: config params passed into constructor instance
    def __init__(self, connection, configuration):
        auth = configuration.get("auth")
        user_name = auth.get('user_name')
        password = auth.get('password')
        host = connection.get('host')
        port = connection.get('port')
        cert = connection.get('cert', None)
        host = str(host)
        port = str(port)
        self.api_client = APIClient(host + ':' + port, user_name, password, cert)
        self.results_connector = BigFixResultsConnector(self.api_client)
        self.status_connector = BigFixStatusConnector(self.api_client)
        self.delete_connector = BigFixDeleteConnector(self.api_client)
        self.query_connector = BigFixQueryConnector(self.api_client)
        self.ping_connector = BigFixPing(self.api_client)
        self.is_async = True

