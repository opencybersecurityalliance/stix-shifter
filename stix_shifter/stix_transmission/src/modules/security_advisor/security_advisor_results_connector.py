from ..base.base_results_connector import BaseResultsConnector
from .utils.stix_pattern_processor import StixPatternProcessor
from .....utils.error_response import ErrorResponder


class SecurityAdvisorResultsConnector(BaseResultsConnector):
    def __init__(self, host, auth ):
        self.host = host
        self.auth = auth
        self.StixPatternProcessor = StixPatternProcessor()

    def create_results_connection(self, searchID , offset , length):

        params = {}
        return_obj = {}
        params["accountID"] =  self.auth.get("accountID")
        params["host"] = self.host

        try :
            params["accessToken"] = self.auth["authToken"].obtainAccessToken()
            
        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"Authorizaion Failed"}, message= str(e))
            return return_obj

        try :
            data  = self.StixPatternProcessor.process(searchID,params)
            return_obj["success"] = True
            return_obj["data"] =  data
            return return_obj

        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"query_failed"}, message= str(e))
            return return_obj
        