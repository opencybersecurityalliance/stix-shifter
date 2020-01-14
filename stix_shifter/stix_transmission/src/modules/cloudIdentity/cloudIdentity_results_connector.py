from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        #FOR TESTING RESULTS TODO delete when done
        self.api_client.create_search(search_id)


        pp = pprint.PrettyPrinter(indent=1)

        response = self.api_client.get_search_results(search_id)
        results = json.loads(response.read())
        return_obj = dict()
        #pp.pprint(results)
        if(response.code == 200):

            return_obj['success'] = True
            return_obj['search_id'] = search_id
            
            #FOR DEMO PURPOSES JSON.DUMP whole object #TODO delete when done testing UDS expects return_obj['data']
            return_obj = results
            return_obj = json.dumps(return_obj)
            #pp.pprint(return_obj)
            #TODO what is actually responded uncomment when done testing
            #return_obj['data'] = json.dumps(results)

        else:
            ErrorResponder.fill_error(return_obj, results, ['message'])
        
        return return_obj