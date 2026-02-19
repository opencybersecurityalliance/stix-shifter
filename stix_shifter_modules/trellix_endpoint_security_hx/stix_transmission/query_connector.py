from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json


class InvalidHostSetNameException(Exception):
    pass


class QueryConnector(BaseQueryConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_query_connection(self, query):
        """
        Fetches the host set details and creates enterprise search on the corresponding host set.
        :param query:
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            if not self.api_client.headers.get('X-FeApi-Token'):
                token_obj = await self.__get_token()
                if token_obj:
                    return token_obj

            if isinstance(query, str):
                query = json.loads(query)
            host_set_name = query['host_set']['_id']
            host_object = await self.fetch_host_details(host_set_name)
            if not host_object.get('host_set_id'):
                return host_object
            query['host_set']['_id'] = host_object['host_set_id']

            response = await self.api_client.create_search(query)
            response_content = response.read().decode('utf-8')
            response_code = response.code
            if response_code == 201:
                response_content = json.loads(response_content)
                return_obj['success'] = True
                return_obj['search_id'] = f"{str(response_content['data']['_id'])}:{host_set_name}"
            else:
                return_obj = self.handle_api_exception(response_code, response_content)

        except Exception as err:
            self.logger.error(f'Error when creating search in Trellix Endpoint Security HX:{err}')
            return_obj = self.handle_api_exception(None, str(err))

        await self.api_client.delete_token()
        return return_obj

    async def __get_token(self):
        """
        Generate a new API token
        :return:
        """
        return_obj = {}
        response = await self.api_client.generate_token()
        if response.code == 204 and response.headers.get('X-FeApi-Token'):
            self.api_client.headers['X-FeApi-Token'] = response.headers['X-FeApi-Token']
            if self.api_client.headers.get('Authorization'):
                self.api_client.headers.pop('Authorization')
        else:
            return_obj = self.handle_api_exception(response.code, response.read().decode('utf-8'))
        return return_obj

    async def fetch_host_details(self, host_set_name):
        """
        Fetches the host set id for the input host set name
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            host_response = await self.api_client.get_host_set(host_set_name)
            host_response_content = host_response.read().decode('utf-8')
            host_response_code = host_response.code
            if host_response_code == 200:
                return_obj = QueryConnector.fetch_success_response(return_obj, host_response_content)
            else:
                return_obj = self.handle_api_exception(host_response_code, host_response_content)

        except InvalidHostSetNameException:
            return_obj = self.handle_api_exception(100, "Invalid Host Set Name")

        except Exception as e:
            self.logger.error('Error while fetching host set details in Trellix Endpoint Security : %s', e)
            return_obj = self.handle_api_exception(None, str(e))
        return return_obj

    @staticmethod
    def fetch_success_response(return_obj, host_response_content):
        """
        Creates the return object with success status and host set id
        :param return_obj:
        :param host_response_content:
        :return: dict
        """
        host_response_content = json.loads(host_response_content)
        return_obj['success'] = True
        entries = host_response_content.get('data', {}).get('entries', [])
        if entries:
            return_obj['host_set_id'] = entries[0]['_id']
        else:
            raise InvalidHostSetNameException()
        return return_obj

    def handle_api_exception(self, code, response_data):
        """
        create the exception response
        :param code, int
        :param response_data, dict
        :return: return_obj, dict
        """
        return_obj = {}
        try:
            response_data = json.loads(response_data)
            if response_data.get('details', []):
                message = response_data['details'][0]['message']
            else:
                message = response_data.get('message')
        except json.JSONDecodeError:
            message = response_data

        if 'exceeded limit on existing searches' in message.lower():
            if response_data.get('details', []) and response_data['details'][0]['details']['existing_search_limit']:
                message = (f"The total search limit - {response_data['details'][0]['details']['existing_search_limit']}"
                           f" is reached. Delete an existing search to create a new one")
            else:
                message = f"The total search limit is reached. Delete an existing search to create a new one"

        response_dict = {'code': code, 'message': message} if code else {'message': message}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
