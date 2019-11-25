from ..base.base_results_connector import BaseResultsConnector
import json
from .utils.sa_occurence_finder import query_func
from .utils.sa_findings_api import get_all_occurences
from .utils.StixPatternParser import StixPatternParser
from .....utils.error_response import ErrorResponder


class SecurityAdvisorResultsConnector(BaseResultsConnector):
    def __init__(self, host, auth ):
        self.host = host
        self.auth = auth
        self.StixPatternParser = StixPatternParser()

    def create_results_connection(self, searchID , offset , length):

        params = {}
        params["accountID"] =  self.auth["accountID"]
        params["accessToken"] =  self.auth["authToken"].obtainAccessToken()
        params["host"] = self.host

        return_obj = {}

        try :
            data  = self.StixPatternParser.parse(searchID,params)
            return_obj["success"] = True
            return_obj["data"] =  data
            return return_obj

        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"query_failed"}, message= str(e))
            return return_obj
        