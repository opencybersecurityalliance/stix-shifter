from ..base.base_connector import BaseConnector
from .security_advisor_ping import SecurityAdvisorPing
from .security_advisor_query_connector import SecurityAdvisorQueryConnector
from .security_advisor_status_connector import SecurityAdvisorStatusConnector
from .security_advisor_results_connector import SecurityAdvisorResultsConnector
from .security_advisor_delete_connector import SecurityAdvisorDeleteConnector


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        auth = configuration.get("auth")
        host = connection.get("host")

        self.query_connector = SecurityAdvisorQueryConnector(host, auth)
        self.status_connector = SecurityAdvisorStatusConnector(host, auth)
        self.results_connector = SecurityAdvisorResultsConnector(host, auth)
        self.delete_connector = SecurityAdvisorDeleteConnector(host, auth)
        self.is_async = False
        self.ping_connector = SecurityAdvisorPing(host, auth)
