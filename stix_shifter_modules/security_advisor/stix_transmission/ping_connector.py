from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
import requests
from stix_shifter_utils.utils.error_response import ErrorResponder
from .auth import Auth


class PingConnector(BasePingConnector):
    def __init__(self, host, auth):
        self.host = host
        self.auth = auth
        api_key = auth.get("apiKey")
        self.auth_token = Auth(api_key)

    def ping_connection(self):
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
