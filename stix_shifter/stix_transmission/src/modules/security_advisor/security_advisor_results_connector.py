from ..base.base_results_connector import BaseResultsConnector
import json
import requests

class SecurityAdvisorResultsConnector(BaseResultsConnector):
    def __init__(self, host, auth ):
        self.host = host
        self.auth = auth

    def create_results_connection(self, providerID , offset , length):

        # url = self.host + self.auth["accountID"] + "/providers/" + providerID + "/occurrences"

        url = self.host + self.auth["accountID"] + "/providers/" + providerID + "/occurrences" +"?page_size=" + str(length) + "&page_token=" + offset

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