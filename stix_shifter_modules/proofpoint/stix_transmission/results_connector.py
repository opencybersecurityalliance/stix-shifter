import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import ast

class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        try:
            min_range = offset
            max_range = offset + length
            # Grab the response, extract the response code, and convert it to readable json
            response = self.api_client.get_search_results(search_id)
            #update response with is_multipart : True
            response_code = response.code
            response_txt = response.read()
            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                try:
                    try:
                        response_txt = response.read().decode('utf-8')
                    except:
                        pass
                    data= json.loads(response_txt)
                    newdata = list()
                    for key, value in data.items():
                        if isinstance(value, list) and value:
                            newdata+=value

                    # slice of the data count according to offset values
                    if newdata and max_range > 0 and len(newdata) > max_range:
                        newdata = newdata[:max_range]

                    return_obj['data'] = newdata

                except json.decoder.JSONDecodeError as e:
                    return_obj['success'] = False

            else:
                return_obj['success'] = False
                # ErrorResponder.fill_error(return_obj, response_dict, ['message'])
                ErrorResponder.fill_error(return_obj,
                                          str(response_code) + ":" + str(response_txt.decode("utf-8")),
                                          ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            raise
