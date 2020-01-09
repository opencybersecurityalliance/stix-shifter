from ..base.base_connector import BaseConnector
from .cloudIdentity_results_connector import CloudIdentityResultsConnector
from .cloudIdentity_ping import CloudIdentityPing
from .cloudIdentity_query_connector import CloudIdentityQueryConnector
from .cloudIdentity_status_connector import CloudIdentityStatusConnector
from .apiclient import APIClient
from ..base.base_status_connector import Status
import json

class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.apiclient = APIClient(connection, configuration)
        self.ping_connector = CloudIdentityPing(self.apiclient)
        self.results_connector = CloudIdentityResultsConnector(self.apiclient)
        self.status_connector = CloudIdentityStatusConnector(self.apiclient)
        self.query_connector = CloudIdentityQueryConnector(self.apiclient)
        self.is_async = False



 