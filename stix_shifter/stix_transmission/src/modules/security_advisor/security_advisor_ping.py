from ..base.base_ping import BasePing
import requests
from .....utils.error_response import ErrorResponder
from .security_advisor_auth import SecurityAdvisorAuth


class SecurityAdvisorPing(BasePing):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth
        api_key = auth.get("apiKey")
        self.auth_token = SecurityAdvisorAuth(api_key)

    def ping(self):
        return_obj = {}        
        header = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }


        url = self.host + "/" + self.auth["accountID"] + "/providers"
        try:
            authorization = "Bearer {}".format(self.auth_token.obtainAccessToken())

            header["Authorization"] = authorization
            
        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"Authorizaion Failed"}, message=str(e))
            return return_obj

        try:
            response = requests.get(url,headers= header)
            response_code = response.status_code

            if (response_code == 200):
                return_obj["success"] = True
            else:
                ErrorResponder.fill_error(return_obj, {'code':"service_not_availiable"}, message= "Status Code is " + str(response_code))
            return return_obj

        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"service_not_availiable"}, message= str(e))
        return return_obj
