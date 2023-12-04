import ast
from http.client import responses
import json
from stix_shifter_modules.tanium.stix_transmission.tanium_config import TaniumConfig

from stix_shifter_utils.utils.error_response import ErrorCode

from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseJsonSyncConnector):
    _QUERY_ENDPOINT = 'plugin/products/threat-response/api/v1/alerts?'
    _QUERY_OFFSET = '&offset='
    
    def __init__(self, connection, configuration):
        self.config = TaniumConfig(connection, configuration)
        self.headers = {'session': self.config.getAccessToken(),
            'Content-Type': 'application/json',
            'Accept': 'application/json'}
        self.api_client = RestApiClientAsync(self.config.getHostname(), port=self.config.getPort(), headers=self.headers)
        self.final_results = list()
        self.current_offset = 0
        self.return_obj = dict()
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
    
    async def ping_connection(self):
        self.return_obj['success'] = False
        try:
            await self.query_tanium_api(self._QUERY_ENDPOINT)
            self.return_obj['success'] = True
        except Exception:
            self.logger.error('error when pinging Tanium datasource {}:'.format(self.return_obj["error"]))
        return self.return_obj
        

    async def create_results_connection(self, query, offset, limit):
        self.return_obj['success'] = False
        self.return_obj["data"] = {}
        offset = int(offset)
        limit = int(limit)
        #Initalize values
        self.current_offset = offset
        per_query_limit = 100
        
        if(limit < per_query_limit):
            per_query_limit = limit
        
        try:
            results = await self.get_results(per_query_limit, query, self.current_offset) 
            #Are we done?
            while(len(self.final_results) < limit and len(results) > 0):
                results = await self.get_results(per_query_limit, query, self.current_offset)
                
            self.return_obj["data"] = self.final_results
            self.return_obj['success'] = True
            self.return_obj['metadata'] = self.return_obj['metadata'] = {"next_offset": self.current_offset, "total_result_count": len(self.final_results)}
            
        except Exception as err:
            self.logger.error('error when connecting to the Tanium datasource {}:'.format(self.return_obj["error"]))
        return self.return_obj
        
    async def get_results(self, per_query_limit, query, current_offset):
        #Create initial query
        if(query != ""):
            current_query = "%s%s&limit=%s&offset=%s&expand=intelDoc" % (self._QUERY_ENDPOINT, query, per_query_limit, current_offset)
        else:
            current_query = "limit=%s&offset=%s&expand=intelDoc" % (self._QUERY_ENDPOINT, per_query_limit, current_offset)
            
        response_data = await self.query_tanium_api(current_query)
        response_data_as_json = json.loads(response_data.content.decode('utf-8'))
        self._add_results_to_final_dataset(response_data_as_json["data"])
        return response_data_as_json["data"]
        
    def _add_results_to_final_dataset(self, current_query_results):
        for batch_of_results in current_query_results:
            batch_of_results["details"] = json.loads(batch_of_results["details"])
            self.final_results.append(batch_of_results)
        self.current_offset = self.current_offset + len(current_query_results)
            

    async def query_tanium_api(self, current_query):
        response_dict = dict()
        try:
            response_dict = await self.api_client.call_api(current_query, 'GET', headers=self.headers, data={})
        except Exception as err:
            ErrorResponder.fill_error(self.return_obj, message=str(err), connector=self.connector)
            raise

        try:
            response_code = response_dict.code
            if response_code == 200:
                return response_dict
            else:
                content_as_dict = ast.literal_eval(response_dict.content.decode("utf-8"))
                if("Message" in content_as_dict):
                    ErrorResponder.fill_error(self.return_obj, message=content_as_dict["Message"], connector=self.connector)
                elif("errors" in content_as_dict):
                    ErrorResponder.fill_error(self.return_obj, message=content_as_dict["errors"][0]["description"], connector=self.connector)
                raise
        except Exception:
            self._handle_exceptions(response_dict, content_as_dict)
            raise
        
    def _handle_exceptions(self, response_dict, content_as_dict):
        if("code" in self.return_obj and self.return_obj["code"] == "unknown"):
            error_message = "tanium connector error => Error code|message : " + str(response_dict.code) + "|" + str(responses[response_dict.code])
            if("Message" in content_as_dict):
                error_message = error_message + ". Request message : " + content_as_dict["Message"] + "."
                self.return_obj["error"] = error_message
            elif("errors" in content_as_dict):
                error_message = error_message + ". Request message : " + content_as_dict["errors"][0]["description"] + "."
                self.return_obj["error"] = error_message
            
            if(response_dict.code == 401 or response_dict.code == 407):
                self.return_obj["code"] = ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value
            elif(response_dict.code == 403):
                self.return_obj["code"] = ErrorCode.TRANSMISSION_FORBIDDEN.value
            elif(response_dict.code == 500 or response_dict.code == 501 or response_dict.code == 502  or response_dict.code == 503  or response_dict.code == 504):
                self.return_obj["code"] = ErrorCode.TRANSMISSION_CONNECT.value
            elif(response_dict.code == 400 or response_dict.code == 404 or response_dict.code == 405  or response_dict.code == 411):
                self.return_obj["code"] = ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value
            elif(response_dict.code == 429):
                self.return_obj["code"] = ErrorCode.TRANSMISSION_TOO_MANY_REQUESTS.value
        elif("code" not in self.return_obj):
            self.return_obj["error"] = "An unexpected format was returned by the API."
            self.return_obj["code"] = ErrorCode.TRANSMISSION_UNKNOWN.value