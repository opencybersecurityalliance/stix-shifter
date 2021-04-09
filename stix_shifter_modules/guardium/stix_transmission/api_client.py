from .guard_utils import GuardApiClient
from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper
from stix_shifter_utils.utils import logger
from requests.models import Response
import json 
import base64

class APIClient():

    def __init__(self, connection, configuration):

        # Placeholder client to allow dummy transmission calls.
        # Remove when implementing data source API client.
        url = "https://"+connection["host"]+":"+str(connection.get('port', ''))
        self.client = GuardApiClient(connection["client_id"], url, connection["client_secret"],
                                     configuration["auth"]["username"], configuration["auth"]["password"])

    def ping_data_source(self):
        # Pings the data source
        if self.client.validate_response(self.client.request_token(), "", False):
            return {"code": 200, "success": True}
        else:
            return {"success": False}

    def get_search_status(self, search_id):
        # Check the current status of the search
        return {"code": 200, "status": "COMPLETED"}
    
    def get_status(self, search_id):
        # It is a synchronous connector.
        # return {"code": 200, "status": "COMPLETED"}
        respObj = Response()
        respObj.code = "200"
        respObj.error_type = ""
        respObj.status_code = 200
        content = '{"search_id": "' + search_id + \
            '", "progress":"Completed", "status":"COMPLETED", "data": {"message":"Completed for the search id provided."}}'
        respObj._content = bytes(content, 'utf-8')
        return ResponseWrapper(respObj)
   
    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

    def create_search(self, query_expression):
        respObj = Response()
        respObj.code = "401"
        respObj.error_type = ""
        respObj.status_code = 401
        # print("query="+query_expression)
        if (self.client.access_token):
            self.query = query_expression
            response = self.build_searchId()
            if (response != None):
                respObj.code = "200"
                respObj.error_type = ""
                respObj.status_code = 200
                content = '{"search_id": "' + \
                    str(response) + \
                    '", "data": {"message":  "Search id generated."}}'
                respObj._content = bytes(content, 'utf-8')
            else:
                respObj.code = "404"
                respObj.error_type = "Not found"
                respObj.status_code = 404
                respObj.message = "Could not generate search id."
        else:
            respObj.error_type = "Unauthorized: Access token could not be generated."
            respObj.message = "Unauthorized: Access token could not be generated."
#
        return ResponseWrapper(respObj)
        
    def build_searchId(self):
        # It should be called only ONCE when transmit query is called
        # Structure of the search id is
        # '{"query": ' + json.dumps(self.query) + ', "credential" : ' + json.dumps(self.credential) + '}'
        s_id = None

        if(self.query is None):
            raise IOError(3001, 
            "Could not generate search id because 'query' or 'authorization token' or 'credential info' is not available.")

        else:
            id_str = '{"query": ' + json.dumps(self.query) + ', "target" : "' + self.client.url + '", "user":"'+self.client.user+'"}'
            # print(id_str)
            id_byt = id_str.encode('utf-8')
            s_id = base64.b64encode(id_byt).decode()
            self.search_id=s_id

        # print(s_id)
        return s_id


    def get_search_results(self, search_id,  index_from=None, fetch_size=None):
            # Sends a GET request from guardium
        # This function calls Guardium to get data
        
        if (self.client.access_token):
            self.search_id=search_id
            self.decode_searchId()
            indx = int(index_from)+1
            fsize = int(fetch_size)+1
            if "reportName" in self.query:
                response = self.client.handle_report(self.query, indx, fsize)
            if "category" in self.query:
                # print("TADA")
                response = self.client.handle_qs(self.query, indx, fsize)
            status_code = response.status_code
#           Though the connector gets the authorization token just before fetching the actual result
#           there is a possibility that the token returned is only valid for a second and response_code = 401
#           is returned.  Catch that situation (though remote) and process again.
            if status_code != 200:
                error_msg = json.loads(str(response.read(), 'utf-8'))
                error_code = error_msg.get('error', None)
                if status_code == 401 and error_code == "invalid_token":
                    self.authorization = None
                    if (self.client.get_token()):
                        response = self.client.handle_report(self.query, index_from, fetch_size)
                        status_code = response.response.status_code
                    else:
                        raise ValueError(3002, "Authorization Token not received ")

# Now START and STOP are optional -- A situation can occur that data set can be empty -- handle this situation here
            if status_code == 200:
#
# Determine if the response is empty if empty Guardium sends {"ID": 0,
# "Message": "ID=0 The Query did not retrieve any records"} 
# Raise an error -->  1010: ErrorCode.TRANSMISSION_RESPONSE_EMPTY_RESULT
                # response_content = self.raiseErrorIfEmptyResult(response)
                return response
            else:
                raise ValueError(1020, "Error -- Status Code is NOT 200!")
        else:
            raise ValueError(3002, "Authorization Token not received ")
    

    def decode_searchId(self):
        # These value (self.credential, self.query) must be present.  self.authorization may not.
        try:
            id_dec64 = base64.b64decode(self.search_id)
            jObj = json.loads(id_dec64.decode('utf-8'))
        except:
            raise IOError(
                3001, "Could not decode search id content - " + self.search_id)

        self.query = json.loads(jObj.get("query", None))
        self.credential = jObj.get("credential", None)
        self.authorization = jObj.get("authorization", None)
        return