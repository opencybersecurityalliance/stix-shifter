from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from .utils.stix_pattern_processor import StixPatternProcessor
from stix_shifter_utils.utils.error_response import ErrorResponder
from .auth import Auth


class ResultsConnector(BaseResultsConnector):
    def __init__(self, host, auth ):
        self.connector = __name__.split('.')[1]
        self.auth = auth
        api_key = auth.get("apiKey")
        self.auth_token = Auth(api_key)
        self.host = self.auth_token.find_location(self.auth["accountID"], host)
        self.StixPatternProcessor = StixPatternProcessor()

    async def create_results_connection(self, searchID , offset , length):

        params = {}
        return_obj = {}
        params["accountID"] =  self.auth.get("accountID")
        params["host"] = self.host

        try:
            params["accessToken"] = self.auth_token.obtainAccessToken()
            
        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"Authorizaion Failed"}, message= str(e), connector=self.connector)
            return return_obj

        try:
            data = self.StixPatternProcessor.process(searchID, params)
            return_obj["success"] = True
            return_obj["data"] =  data
            return return_obj

        except Exception as e:
            ErrorResponder.fill_error(return_obj, {'code':"query_failed"}, message= str(e), connector=self.connector)
            return return_obj
