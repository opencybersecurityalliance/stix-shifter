from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class InvalidResponseException(Exception):
    pass


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):

        """
         Function to create query connection
        :param query: dict, str
        :return: dict
        """
        response_dict = {}
        return_obj = {}
        try:
            response = await self.api_client.create_search(query)
            if isinstance(response, dict):   # return the object, if response code is not 200 in create_rule
                return response              # in api_client
            response_code = response[0].status
            response_text = json.loads(response[1])

            if response_code == 200:
                if 'retrohuntId' in response_text.keys() and 'ruleId' in response_text.keys():
                    return_obj['success'] = True
                    return_obj['search_id'] = f"{response_text['retrohuntId']}:{response_text['ruleId']}"

                else:
                    raise InvalidResponseException

            else:
                response_dict['code'] = response_code
                response_dict['message'] = response_text['error'].get('message')
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except InvalidResponseException:
            response_dict['code'] = 100
            response_dict['message'] = "InvalidResponse"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as q_ex:

            response_dict['message'] = f'cannot parse {q_ex}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as q_ex:
            if "timed out" in str(q_ex):
                response_dict['code'] = 120
                response_dict['message'] = str(q_ex)
            else:
                response_dict['message'] = q_ex
            self.logger.error('error when getting search results: %s', q_ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        return return_obj
