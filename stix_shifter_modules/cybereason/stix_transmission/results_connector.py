from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from json.decoder import JSONDecodeError
import json


class InvalidRequestException(Exception):
    pass


class InternalServerErrorException(Exception):
    pass


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):

        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, query, offset, length):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            offset = int(offset)
            length = int(length)
            if isinstance(query, dict):
                query = json.dumps(query)
            response_wrapper = self.api_client.get_search_results(query)
            if response_wrapper.code == 200:
                return_obj['success'] = True
            elif 399 < response_wrapper.code < 500:
                raise InvalidRequestException(response_wrapper.response.text)
            elif response_wrapper.code == 500:
                raise InternalServerErrorException(response_wrapper.response.text)
            response_dict = json.loads(response_wrapper.read().decode('utf-8'))
            results = self.get_results_data(response_dict)
            return_obj['data'] = results[offset:length]

            # session log out
            response_wrapper = self.api_client.session_log_out(response_wrapper)
            if not response_wrapper.code == 200:
                raise InvalidRequestException(response_wrapper.response.text)

        except JSONDecodeError:
            response_dict['type'] = "AuthenticationError"
            response_dict['message'] = "Authentication Invalid"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj

    def get_results_data(self, response_dict):
        results = []
        for log in response_dict['data']['resultIdToElementDataMap'].values():
            data = {}
            element_dict = {}

            if "simpleValues" in log:
                for key, value in log["simpleValues"].items():
                    data[key] = value["values"][0].replace('\u0000', '')
            if "elementValues" in log:
                for key, value in log["elementValues"].items():
                    if value["elementValues"]:
                        if len(value["elementValues"]) > 1:
                            data[key] = [name["name"] for name in value["elementValues"]]
                        else:
                            data[key] = value["elementValues"][0]["name"]

            element_name = self.get_element_name(response_dict)
            element_dict[element_name] = data
            results.append(element_dict)
        return results

    @staticmethod
    def get_element_name(res_dict):
        """
        Get the name of the element
        :param res_dict: dict, log
        :return: str, element name
        """
        element_name = res_dict['data']['pathResultCounts'][0]['featureDescriptor']['elementInstanceType']
        return element_name
