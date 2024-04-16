from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.expired_token_count = 0

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        """
        data = []
        try:
            result_count, total_records, page_number, page_size = self.handle_metadata_and_page_size(int(offset),
                                                                                                int(length), metadata)
            # Generating jwt token
            jwt_token, return_obj = await self.__get_token()
            if return_obj:
                return return_obj

            remaining_record_count = 0

            while result_count < total_records:
                query_url = f'{query}&page={page_number}&count={page_size}'
                response_wrapper = await self.api_client.get_search_results(query_url, jwt_token)
                response_dict, return_obj = self.handle_api_response(response_wrapper)

                if return_obj:
                    return return_obj

                # Generate a new token only the token_generated_count is 1.
                # If it is more than one, it has already been generated.
                if self.expired_token_count == 1:
                    jwt_token, return_obj = await self.__get_token()
                    self.expired_token_count += 1
                    if return_obj:
                        return return_obj
                    continue

                return_obj['success'] = True
                # remaining records value is less than fetched records.
                if remaining_record_count and remaining_record_count < len(response_dict['result']):
                    data += response_dict['result'][:remaining_record_count]
                    result_count += len(response_dict['result'][:remaining_record_count])
                else:
                    data += response_dict['result']
                    result_count += len(response_dict['result'])

                if len(response_dict['result']) < page_size:
                    page_number = None
                    break

                # calculating remaining records count
                if result_count < total_records:
                    remaining_record_count = total_records - result_count
                else:   # if doesn't have remaining records
                    break

                page_number += 1

            return_obj = self.handle_data(data, metadata, offset, total_records, return_obj)

            if return_obj.get('data'):
                if page_number and result_count < self.api_client.result_limit:
                    return_obj['metadata'] = {"page_number": page_number+1}

        except InvalidMetadataException as ex:
            return_obj = self.handle_api_exception(422, f'Invalid metadata: {str(ex)}')

        except Exception as ex:
            return_obj = self.handle_api_exception(None, str(ex))
        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        Connects to the health_logs API endpoint and confirms connectivity and authentication to the product
        :return: return_object, dict
        """
        try:
            token, return_obj = await self.__get_token()
            if return_obj:
                return return_obj
            response = await self.api_client.ping_data_source(token)
            response_code = response.code
            response_dict = json.loads(response.read().decode('utf-8'))
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.handle_api_exception(response_code, response_dict.get('errorSummary', ''))
        except Exception as ex:
            return_obj = self.handle_api_exception(None, str(ex))
        return return_obj

    async def __get_token(self):
        """
        Generate new token
        :return: token, string
                 return_obj, dict
        """
        return_obj = {}
        token = None
        response = await self.api_client.generate_token()
        response_code = response.code
        response_json = json.loads(response.read().decode('utf-8'))
        if response_code != 200:
            return_obj = self.handle_api_exception(response_code, response_json.get('errors', ''))
        else:
            response_header = response.headers
            if 'Authorization' in response_header:
                token = response_header.get('Authorization')
        return token, return_obj

    def handle_api_exception(self, code=None, response_txt=''):
        """
        create the exception response
        :param code, int
        :param response_txt, str
        :return: return_obj, dict
        """
        return_obj = {}
        message = None

        if "'key_name': ['is invalid']" in str(response_txt):
            message = "Invalid Authentication: " + str(response_txt)

        if 'Invalid URL' in str(response_txt):
            message = "Invalid Host: " + str(response_txt)

        if not message:
            message = str(response_txt)

        response_dict = {'code': code, 'message': message}
        self.logger.error('%s error while fetching results: %s', self.connector, message)
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def handle_metadata_and_page_size(self, offset, length, metadata):
        """
        Processing metadata information and page size
        :param offset, int
        :param length, int
        :param metadata, dict
        :return: return_obj, dict
        """
        page_number = 1

        if metadata:
            if isinstance(metadata, dict) and metadata.get('page_number'):
                page_number = int(metadata.get('page_number', 1))
            else:
                # raise exception when metadata doesnt contain jwtToken token
                raise InvalidMetadataException(metadata)

        total_records = offset + length
        page_size = length

        if self.api_client.result_limit < total_records:
            total_records = self.api_client.result_limit

        if self.api_client.max_page_size < page_size:
            page_size = self.api_client.max_page_size

        # for the first api call result_count is zero
        result_count = page_size * (page_number - 1)

        return result_count, total_records, page_number, page_size

    def handle_api_response(self, response_wrapper):
        """
        Handling response codes
        :param response_wrapper, object
        :return: response_dict, dict
                 return_obj, dict
        """
        response_dict = {}
        return_obj = {}
        response = response_wrapper.read().decode('utf-8')
        if response.startswith('{') and response.endswith('}'):
            response_dict = json.loads(response)

        if response_wrapper.code == 200:
            # Handling invalid query exception
            if 'Query is not valid' in response_dict.get('error', ''):
                return_obj = self.handle_api_exception(400, response_dict.get('error'))  # changing response code to 400
            # Handling expired token
        elif response_wrapper.code == 401 and not self.expired_token_count and \
                (response == '' or 'Signature has expired' in response_dict.get('error', {}).get('message', '')):
            self.expired_token_count += 1
        else:
            error = response_dict.get('error', '')
            if response_wrapper.code == 403:
                error = 'Query length is too long or Invalid Query.' + error
            return_obj = self.handle_api_exception(response_wrapper.code, error)
        return response_dict, return_obj

    @staticmethod
    def handle_data(data, metadata, offset, total_records, return_obj):
        """
         Process the data
        :param data, list
        :param metadata, dict
        :param offset, int
        :param total_records, int
        :param return_obj, dict
        :return: return_obj, dict
        """
        if data:
            data = Connector.get_results_data(data)
            if metadata:
                return_obj['data'] = data if data else []
            else:
                return_obj['data'] = data[int(offset): total_records] if data else []
        else:
            if not return_obj.get('error') and return_obj.get('success') is not False:
                return_obj['success'] = True
                return_obj['data'] = []
        return return_obj

    @staticmethod
    def get_results_data(response):
        """
         Preprocessing the response.
        :param response: list
        :return response: list
        """
        for record in response:
            # threat_name is None or '' means finding type is alert"
            if record.get('threat_name') is (None or ''):
                record['threat_name'] = 'alert'
        return response
