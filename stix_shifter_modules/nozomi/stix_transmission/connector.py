from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json
import re


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    NOZOMI_MAX_PAGE_SIZE = 10000

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, query, offset, length, metadata=None):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :param metadata: dict
        :return: return_obj, dict
        """
        return_obj = {}
        data = []
        response_dict = {}
        jwt_token = None
        local_result_count = 0
        token_generated = False
        try:
            if metadata:
                if isinstance(metadata, dict) and metadata.get('jwtToken'):
                    jwt_token = metadata.get('jwtToken')
                    next_url = metadata.get('next_url')
                    result_count = int(metadata.get('result_count'))
                else:
                    # raise exception when metadata doesnt contain jwtToken token
                    raise InvalidMetadataException(metadata)
            else:
                result_count, next_url = 0, None

            total_records = int(offset) + int(length)
            if self.api_client.result_limit < total_records:
                total_records = self.api_client.result_limit

            if total_records <= Connector.NOZOMI_MAX_PAGE_SIZE:
                page_size = total_records
            else:
                page_size = Connector.NOZOMI_MAX_PAGE_SIZE

            if not jwt_token:
                jwt_token = await self.get_token()

            if (result_count == 0 and next_url is None) or (next_url and result_count < self.api_client.result_limit):
                while result_count < total_records:
                    if next_url:
                        query_url = next_url
                    else:
                        query_url = f'{query}&page=1&count={page_size}'
                    response_wrapper = await self.api_client.get_search_results(query_url, jwt_token)
                    response = response_wrapper.read().decode('utf-8')
                    if response:
                        response_dict = json.loads(response)
                    if response_wrapper.code == 200:
                        # Handling invalid query exception
                        if 'Query is not valid' in response_dict.get('error', ''):
                            return_obj = self.exception_response(response_wrapper.code, response_dict.get('error'))
                            data = []
                            break

                        return_obj['success'] = True
                        data += response_dict['result']
                        result_count += len(response_dict['result'])
                        local_result_count += len(response_dict['result'])

                        if response_dict['total'] <= result_count or len(response_dict['result']) == 0:
                            next_url = None
                            break
                        # parsing the next_url
                        page = re.findall(r'page=([^>]*?)&', query_url)[0]
                        next_url = re.sub(r'page=([^>]*?)&', f'page={str(int(page) + 1)}&', query_url)

                        if not metadata and result_count < total_records:
                            remaining_records = total_records - result_count
                        elif metadata and local_result_count < total_records:
                            remaining_records = total_records - local_result_count
                        else:
                            break

                        if remaining_records > Connector.NOZOMI_MAX_PAGE_SIZE:
                            page_size = Connector.NOZOMI_MAX_PAGE_SIZE
                        else:
                            page_size = remaining_records
                    # Handling expired token
                    elif response_wrapper.code == 401 and not token_generated and \
                            (response == '' or
                             'Signature has expired' in response_dict.get('error', {}).get('message', '')):
                        jwt_token = await self.get_token()
                        token_generated = True
                        continue
                    else:
                        error = response_dict.get('error', '')
                        if response_wrapper.code == 403:
                            error = 'Query length is too long or Invalid Query'
                        return_obj = self.exception_response(response_wrapper.code, error)
                        data = []
                        break

                if data:
                    data = self.get_results_data(data)
                    if metadata:
                        return_obj['data'] = data if data else []
                    else:
                        return_obj['data'] = data[int(offset): total_records] if data else []
                    if jwt_token and next_url and result_count < self.api_client.result_limit:
                        return_obj['metadata'] = {"result_count": result_count, "jwtToken": jwt_token,
                                                  "next_url": next_url}
                else:
                    if not return_obj.get('error') and return_obj.get('success') is not False:
                        return_obj['success'] = True
                        return_obj['data'] = []
            else:
                return_obj['success'] = True
                return_obj['data'] = []

        except InvalidMetadataException as ex:
            return_obj = self.exception_response(422, f'Invalid metadata: {str(ex)}')

        except Exception as ex:
            return_obj = self.exception_response(None, str(ex))
        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        try:
            token = await self.get_token()
            response = await self.api_client.ping_data_source(token)
            response_code = response.code
            response_dict = json.loads(response.read().decode('utf-8'))
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.exception_response(response_code, response_dict.get('errorSummary', ''))
        except Exception as ex:
            return_obj = self.exception_response(None, str(ex))
        return return_obj

    async def get_token(self):
        """ Generate new token"""
        response = await self.api_client.generate_token()
        response_code = response.code
        response_txt = response.read().decode('utf-8')
        response_json = json.loads(response_txt)
        if response_code == 200:
            response_header = response.headers
            if 'Authorization' in response_header:
                token = response_header.get('Authorization')
            return token
        raise Exception(response_json['errors'])

    def exception_response(self, code=None, response_txt=''):
        """
        create the exception response
        :param code, int
        :param response_txt, str
        :return: return_obj, dict
        """
        return_obj = {}
        message = None

        if 'Query is not valid' in response_txt:
            code = 400
            message = 'Query is not valid'

        if code == 401 and not response_txt:
            message = 'Authentication failed'

        if not code:
            if "'key_name': ['is invalid']" in response_txt:
                code = 401
                message = "Invalid Authentication: " + response_txt
            elif "timeout_error" in response_txt:
                code = 408
            elif 'Invalid URL' in response_txt:
                code = 408
                message = "Invalid Host: " + response_txt

        if not message:
            message = str(response_txt)

        response_dict = {'code': code, 'message': message}
        self.logger.error('%s error while fetching results: %s', self.connector, message)
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
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
            if record.get('threat_name') is None:
                record['threat_name'] = 'alert'
        return response
