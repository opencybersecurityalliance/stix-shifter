from ..base.base_connector import BaseConnector
from .security_advisor_ping import SecurityAdvisorPing
from .security_advisor_query_connector import SecurityAdvisorQueryConnector
from .security_advisor_status_connector import SecurityAdvisorStatusConnector
from .security_advisor_results_connector import SecurityAdvisorResultsConnector

from .security_advisor_auth import SecurityAdvisorAuth
import os

class Connector(BaseConnector):
    def __init__(self, connection, configuration ):
        
        auth  = {}

        accountID = configuration.get("ibmCloudAccountID")
        apiKey = configuration.get("ibmCloudApiKey") 
        host = configuration.get("saAPIEndpoint")

        if( not accountID or not apiKey or not host ):
            raise Exception("accountID or APIKEY or Host not present !!")

        auth["accountID"] = accountID
        authToken = SecurityAdvisorAuth(apiKey).obtainAccessToken()
        auth["authToken"] = authToken


        self.query_connector = SecurityAdvisorQueryConnector(host, auth)
        self.status_connector = SecurityAdvisorStatusConnector(host, auth)
        self.results_connector = SecurityAdvisorResultsConnector(host, auth)
        self.is_async = True
        self.ping_connector = SecurityAdvisorPing(host, auth)
