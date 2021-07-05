import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseResultsConnector):
    max_limit = 50

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
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length
        try:
            if self.init_error:
                self.logger.error("Token Generation Failed:")
                return self.init_error
            # Grab the response, extract the response code, and convert it to readable json
            if length <= self.max_limit:
                # $(offset) param not included as data source not support this
                response_dict = self.api_client.run_search(quary_expr, total_records, self.access_token)
            else:
                response_dict = self.api_client.run_search(quary_expr, self.max_limit, self.access_token)
            response_code = response_dict.code
            # Construct a response object
            response_dict = json.loads(response_dict.read())
            # print(response_dict)
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_dict['data']
                next_page_link = response_dict['pagination']['next_link']
                while len(return_obj['data']) < total_records and next_page_link:
                    try:
                        response = self.api_client.next_page_run_search(next_page_link)
                        response_code = response.code
                        response_dict = json.loads(response.read())
                        if response_code == 200:
                            return_obj['data'].extend(response_dict['data'])
                        else:
                            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'])
                    except KeyError:
                        break
                # slice the records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:total_records]
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





