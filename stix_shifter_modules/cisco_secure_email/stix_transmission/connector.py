from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    EMAIL_MAX_PAGE_SIZE = 100

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
        result_count = 0
        response_dict = {}
        jwt_token = None
        try:
            if metadata:
                if isinstance(metadata, dict) and metadata.get('jwtToken'):
                    jwt_token = metadata.get('jwtToken')
                else:
                    # raise exception when metadata doesnt contain jwtToken token
                    raise InvalidMetadataException(metadata)
            total_records = int(offset) + int(length)
            if self.api_client.result_limit < total_records:
                total_records = self.api_client.result_limit
            if total_records <= Connector.EMAIL_MAX_PAGE_SIZE:
                page_size = total_records
            else:
                page_size = Connector.EMAIL_MAX_PAGE_SIZE
            if not jwt_token:
                jwt_token = await self.get_token()
            result_offset = int(offset)
            while result_count < total_records:
                limit = f'&limit={page_size}&offset={result_offset}'
                response_wrapper = await self.api_client.get_search_results(query + limit, jwt_token)
                response_dict = json.loads(response_wrapper.read().decode('utf-8'))
                if response_wrapper.code == 200:
                    return_obj['success'] = True
                    data += response_dict['data']
                    result_count += len(response_dict['data'])
                    remaining_records = total_records - result_count
                    if remaining_records > Connector.EMAIL_MAX_PAGE_SIZE:
                        page_size = Connector.EMAIL_MAX_PAGE_SIZE
                    else:
                        page_size = remaining_records
                    # Exit the loop if there are no more records to fetch
                    # if no more records to fetch API returns empty data
                    if len(response_dict['data']) == 0:
                        break
                    result_offset += len(response_dict['data'])
                elif response_wrapper.code == 401 and response_dict['error']['message'] in ['ExpiredSignatureError.',
                                                                                            'InvalidTokenError.']:
                    jwt_token = await self.get_token()
                    continue
                else:
                    return_obj = self.exception_response(response_wrapper.code, response_dict['error'])
                    data = []
                    break
            if data:
                data = self.add_is_multipart(data)
                if metadata:
                    return_obj['data'] = data if data else []
                else:
                    return_obj['data'] = data[int(offset): total_records] if data else []
                if jwt_token:
                    return_obj['metadata'] = {"jwtToken": jwt_token}
            else:
                if not return_obj.get('error') and return_obj.get('success') is not False:
                    return_obj['success'] = True
                    return_obj['data'] = []

        except InvalidMetadataException as ex:
            response_dict['code'] = 100
            response_dict['message'] = f'Invalid metadata: {str(ex)}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as ex:
            if "server timeout_error" in str(ex):
                response_dict['code'] = 503
            elif "timeout_error" in str(ex):
                response_dict['code'] = 408
            elif "X509" in str(ex):
                response_dict['code'] = 101
                response_dict['message'] = "Invalid Self Signed Certificate: "+str(ex)
            if not response_dict.get('message'):
                response_dict['message'] = str(ex)
            self.logger.error('error while fetching results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        response_dict = {}
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
            if "server timeout_error" in str(ex):
                response_dict['code'] = 503
            elif "timeout_error" in str(ex):
                response_dict['code'] = 408
            elif "X509" in str(ex):
                response_dict['code'] = 101
                response_dict['message'] = "Invalid Self Signed Certificate: "+str(ex)
            if not response_dict.get('message'):
                response_dict['message'] = str(ex)
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    async def get_token(self):
        """ Generate new token"""
        response = await self.api_client.generate_token()
        response_code = response.code
        response_txt = response.read().decode('utf-8')
        response_json = json.loads(response_txt)
        if response_code == 200:
            if 'data' in response_json and 'jwtToken' in response_json['data']:
                token = response_json['data'].get('jwtToken')
            return token
        raise Exception(response_json['error'])

    def exception_response(self, code, response_txt):
        """
        create the exception response
        :param code, int
        :param response_txt, dict
        :return: return_obj, dict
        """
        return_obj = {}
        response_dict = {'code': code, 'message': str(response_txt)}
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    @staticmethod
    def add_is_multipart(data):
        """
        add is_multipart field
        :param data, list
        :return: data, list
        """
        for row in data:
            if row['attributes'].get('recipient') or row['attributes'].get('friendly_from') or \
                    row['attributes'].get('sender') or row['attributes'].get('subject'):
                row['attributes']['is_multipart'] = True
        return data
