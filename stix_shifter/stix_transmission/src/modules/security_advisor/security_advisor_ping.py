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

        return_obj = {}

        try :
            response = requests.get(url,headers= header)
            response_code = response.status_code

            if ( response_code == 200 ):
                return_obj["success"] = True
            else:
                return_obj["success"] = False
                return_obj["Exception"] =  str(Exception("Ping Failed!"))
            return return_obj

        except Exception as e:
            return_obj["success"] = False
            return_obj["Exception"] = str(e)

        return return_obj
