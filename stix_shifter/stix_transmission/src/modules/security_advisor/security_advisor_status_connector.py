from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status

import requests


class SecurityAdvisorStatusConnector(BaseStatusConnector):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    def create_status_connection(self, providerID):
    
        url = self.host + self.auth["accountID"] + "/providers/" + providerID + "/notes"

        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization' : 'Bearer '  + self.auth["authToken"],
        }

        dict = {}

        try :
            r = requests.get(url,headers= header)
            dict["status"] = r.json()

            if( r.status_code == 200 ):
                dict["success"] = True
            else:
                dict["success"] = False

            return dict

        except Exception as e :

            dict["success"] = False
            dict["Exception"] = e

        return dict
