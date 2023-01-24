from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from .utils.stix_pattern_processor import StixPatternProcessor
from stix_shifter_utils.utils.error_response import ErrorResponder
from .api_client import APIClient


class ResultsConnector(BaseJsonResultsConnector):
    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.host = connection.get("host")
        self.auth = configuration.get("auth")
        self.api_client = APIClient(connection, configuration)

        self.host = self.api_client.find_location(self.auth["accountID"], self.host)
        self.StixPatternProcessor = StixPatternProcessor()


    async def create_results_connection(self, searchID , offset , length):
        params = {}
        return_obj = {}
        params["accountID"] =  self.auth.get("accountID")
        params["host"] = self.host

        try:
            params["accessToken"] = self.api_client.obtainAccessToken()
            
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
