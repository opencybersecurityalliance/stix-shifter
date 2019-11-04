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

        try :
            r = requests.get(url,headers= header)
            if( r.status_code == 200 ):
                return 'Success'
            else :
                return 'Failure'


        except Exception :
            return 'Failure'
