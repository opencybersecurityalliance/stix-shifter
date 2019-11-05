from ..base.base_ping import BasePing
import requests

class SecurityAdvisorPing(BasePing):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    def ping(self):
        
        url = self.host + self.auth["accountID"] + "/providers"
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization' : 'Bearer '  + self.auth["authToken"] ,
        }

        dict = {}

        try :
            r = requests.get(url,headers= header)

            response_code = r.status_code
            dict["response_code"] = response_code

            if ( response_code == 200 ):
                dict["success"] = True
            else:
                dict["success"] = False

            return dict

        except Exception as e:
            dict["success"] = False
            dict["Exception"] = e

        return dict
