import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.init_error = None
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.token_resp = self.get_token()
        if self.token_resp["code"] == 200:
            self.access_token = self.token_resp["access_token"]
        else:
            self.init_error = self.token_resp

    def create_results_connection(self, quary_expr, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            if self.init_error:
                self.logger.error("Token Generation Failed:")
                return self.init_error
            # Grab the response, extract the response code, and convert it to readable json
            response_dict = self.api_client.run_search(quary_expr, min_range, max_range, self.access_token)
            response_code = response_dict.code
            # Construct a response object
            response_dict = json.loads(response_dict.read())
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            import traceback
            self.logger.error(traceback.print_stack())
            raise

    def get_token(self):
        return_obj = dict()
        try:
            response_dict = self.api_client.generate_token()
            response_code = response_dict.code
            response_dict = json.loads(response_dict.read())
            return_obj["code"] = response_code
            if response_code == 200:
                return_obj["access_token"] = response_dict["access_token"]
            else:
                return_obj["message"] = response_dict["status"]["message"]
        except Exception as e:
            ErrorResponder.fill_error(return_obj, message='unexpected exception')
            self.logger.error('error while generating access token: {}'.format(e))
        return return_obj





