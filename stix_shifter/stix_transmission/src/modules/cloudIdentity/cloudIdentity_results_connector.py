from ..base.base_connector import BaseConnector
from ..base.base_results_connector import BaseResultsConnector
import json
import pprint
from .....utils.error_response import ErrorResponder


class CloudIdentityResultsConnector(BaseConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        response = self.api_client.get_search_results(search_id)
        response_code = response.code

        resp = json.loads(response.read())
        

        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(resp)
        