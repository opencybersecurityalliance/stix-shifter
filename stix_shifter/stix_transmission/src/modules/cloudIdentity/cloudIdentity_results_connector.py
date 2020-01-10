from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        
        pp = pprint.PrettyPrinter(indent=1)
        return_obj = dict()
        request_params = self.parse_query(search_id)
        
        #If input query contains user-account:user_id(MAPS TO)->user_id connector will getUser{user_id} in api_client
        if "user_id" in request_params:
            user_obj = self.api_client.getUser(request_params['user_id'])
            #create return_obj['user-acccount"] based on api response
            return_obj['user-account'] = self.createStixUser(json.loads(user_obj.read()))

        #If input query contains ipv4:value(MAPS TO)->origin -- if present call events and find all ip's that match
        if "origin" in request_params and "FROM" in request_params and "TO" in request_params:
            result = self.api_client.search_events(request_params, "origin")
            pp.pprint(result)
            return_obj = self.eventToStix(result[0])


        retValue = json.dumps(return_obj)
        print(retValue)
        pp.pprint(return_obj)
        return retValue

    #   parse query for key values used to determine which Cloud Identity api calls to make along
    #   With populating the parameters for api call
    

    def createStixUser(self, User):
        stixUser = dict()
        #print(User)
        stixUser['user_id'] = User.get('id', None)
        stixUser['display_name'] = User.get('displayName', None)
        if(stixUser['display_name'] is None):
            stixUser['display_name'] = User.get('name').get('formatted', None)
        stixUser['account_login'] = User.get('userName', None)
        stixUser['account_created'] = User.get('meta').get('created', None)
        stixUser['account_last_login'] = User.get('urn:ietf:params:scim:schemas:extension:ibm:2.0:User').get('lastLogin')
        if "emails" in User:
            stixUser['email-addr'] = self.createStixEmailfromUser(User)

        return stixUser

    def createStixEmailfromUser(self, User):

        stixEmail = dict()
        for index in User.get('emails'):
            stixEmail['value'] = index.get('value')
            stixEmail['display_name'] = User.get('displayName', None)
            if(stixEmail['display_name'] is None):
                stixEmail['display_name'] = User.get('name').get('formatted', None)
          
        return stixEmail

    def createStixIpv4(self, JObj):
        stixObj = dict()
        stixObj['value'] = JObj['origin']
        return stixObj

    def eventToStix(self, eventObj):
        return_obj = dict()
        #if user account is linked to event search id and create user-account stixObj
        if "targetid" in eventObj:
            user_obj = self.api_client.getUser(eventObj['targetid'])
            #create return_obj['user-acccount"] based on api response
            return_obj['user-account'] = self.createStixUser(json.loads(user_obj.read()))
        if "origin" in eventObj:
            return_obj['ipv4-addr'] = self.createStixIpv4(eventObj)
        if "email-addr" in return_obj['user-account']:
            return_obj['email-addr'] = return_obj['user-account'].pop("email-addr", None)
            
        return return_obj

    def parse_query(self, query):
        requests = query.split(' ')
        params = dict()

        #Iterate over query string and assign variables i.e. user-account, ipv4 etc
        for index in range(len(requests)):
            if(requests[index] == "user_id"):
                params["user_id"] = requests[index+2].strip("''")
            elif(requests[index] == "username"):
                params['username'] = requests[index+2].strip("''")
            elif(requests[index] == "origin"):
                params['origin'] = requests[index+2].strip("''")
            elif(requests[index] == "FROM"):
                params['FROM'] = requests[index+1].strip("t''")
            elif(requests[index] == "TO"):
                params['TO'] = requests[index+1].strip("t''")
    
        return params

