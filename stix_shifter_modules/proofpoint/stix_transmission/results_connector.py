import json

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger

class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]


    async def create_results_connection(self, search_id, offset, length):
        try:
            min_range = int(offset)
            max_range = min_range + int(length)

            # Grab the response, extract the response code, and convert it to readable json
            response = await self.api_client.get_search_results(search_id)
            response_code = response.code
            response_txt = response.read()
            # Construct a response object

            return_obj = dict()
            error_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                try:
                    response_txt = response.read().decode('utf-8')
                    data= json.loads(response_txt)
                    newdata = list()
                    for key, value in data.items():
                        if isinstance(value, list) and value:
                            newdata+=value

                    # slice off the data count according to offset values
                    if newdata and max_range > 0 and len(newdata) > max_range:
                        newdata = newdata[min_range:max_range]

                    for msg in newdata:
                        if "messageParts" in msg:
                            msg["is_multipart"] = True
                        else: msg["is_multipart"] = False

                    return_obj['data'] = newdata

                except json.decoder.JSONDecodeError as err:
                    return_obj['success'] = False
                except Exception as err:
                    return_obj['success'] = False
                    self.logger.error('Response decode error: {}'.format(err))

            elif response_code > 200 and response_code <= 204:#empty results
                error_obj['code'] = 2000
            elif response_code == 400:#error from data source
                error_obj['code'] = 4000
            elif response_code == 401:#Authentication error
                error_obj['code'] = 4010
            elif response_code >= 402 and response_code <= 499:#All other client side errors
                error_obj['code'] = 4020
            else:
                #unknown errors
                error_obj['code'] = 7000
            if error_obj:
                error_msg = ""
                try:
                    error_msg = str(response_txt.decode("utf-8"))
                except Exception as err:
                    self.logger.error('Response decode error: {}'.format(err))
                error_obj['message'] = error_msg
                ErrorResponder.fill_error(return_obj,
                                          error_obj,
                                          ['message'], 
                                          connector=self.connector)
                err = 'error when getting search results: {}:{}'.format(str(response_code), error_msg)
                self.logger.error(err)
                # raise NoResultsFoundError(err)
            return return_obj
        except Exception as err:
            self.logger.error('error when getting search results: {}'.format(err))
            raise

class NoResultsFoundError(Exception):
    pass
