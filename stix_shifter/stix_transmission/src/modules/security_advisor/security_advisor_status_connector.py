from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status

import requests


class SecurityAdvisorStatusConnector(BaseStatusConnector):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    def create_status_connection(self, providerID):
    
        url = self.host + self.auth["accountID"] + "/providers/" + providerID

        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization' : 'Bearer '  + self.auth["authToken"],
        }

        try :
            r = requests.get(url,headers= header)
            return r.status_code

        except Exception as e :
            print("some error occured getting Provider !!", str(e))
