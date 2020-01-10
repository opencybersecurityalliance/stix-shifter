from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):

        #TESTING 
        #self.parse_query(search_id)
        #return

        response = self.api_client.get_search_results(search_id)
        response_code = response.code

        pp = pprint.PrettyPrinter(indent=1)

        resp = json.loads(response.read())
    
        return_obj = dict()
        return_obj["user-account"] = self.createStixUser(resp)
        return_obj['email-addr'] = self.createStixEmailfromUser(resp)

        retValue = json.dumps(return_obj)
        print(retValue)
        #pp.pprint(return_obj)


    #parse query for key values
    def parse_query(self, query):
        requests = query.split(' ')
        params = dict()
        print(query)
        

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

        return stixUser

    def createStixEmailfromUser(self, User):

        stixEmail = dict()
        for index in User.get('emails'):
            stixEmail['value'] = index.get('value')
            stixEmail['display_name'] = User.get('displayName', None)
            if(stixEmail['display_name'] is None):
                stixEmail['display_name'] = User.get('name').get('formatted', None)
          
        return stixEmail
