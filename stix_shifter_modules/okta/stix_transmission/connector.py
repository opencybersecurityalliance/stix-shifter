import re
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json


class InvalidMetadataException(Exception):
    pass


class Connector(BaseJsonSyncConnector):
    OKTA_MAX_PAGE_SIZE = 1000
    DOMAIN_PATTERN = re.compile(r'^(?:(?:[a-z0-9]\.)|(?:[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\.))+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$')

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
        local_result_count = 0
        response_dict = {}
        try:
            if metadata:
                if isinstance(metadata, dict) and metadata.get('result_count') and metadata.get('next_page_token'):
                    result_count, next_page_token = metadata['result_count'], metadata['next_page_token']
                    result_count = int(result_count)
                    total_records = int(length)
                    if abs(self.api_client.result_limit - result_count) < total_records:
                        total_records = abs(self.api_client.result_limit - result_count)

                else:
                    # raise exception when metadata doesnt contain result count or next page token
                    raise InvalidMetadataException(metadata)
            else:
                result_count, next_page_token = 0, '0'
                total_records = int(offset) + int(length)
                if self.api_client.result_limit < total_records:
                    total_records = self.api_client.result_limit
            if total_records <= Connector.OKTA_MAX_PAGE_SIZE:
                page_size = total_records
            else:
                page_size = Connector.OKTA_MAX_PAGE_SIZE

            limit = f'&limit={page_size}'
            if (result_count == 0 and next_page_token == '0') or (next_page_token != '0' and result_count <
                                                                  self.api_client.result_limit):
                response_wrapper = await self.api_client.get_search_results(query + limit, next_page_token)
                response_dict = json.loads(response_wrapper.read().decode('utf-8'))
                if response_wrapper.code == 200:
                    return_obj['success'] = True
                    data += response_dict
                    result_count += len(response_dict)
                    local_result_count += len(response_dict)
                    next_page_token = Connector.verify_link_parameter(response_wrapper)
                    # loop until if there is next page link and records fetched is less than total records
                    while next_page_token:
                        if not metadata and result_count < total_records:
                            remaining_records = total_records - result_count

                        elif metadata and local_result_count < total_records:
                            remaining_records = total_records - local_result_count
                        else:
                            break
                        if remaining_records > Connector.OKTA_MAX_PAGE_SIZE:
                            page_size = Connector.OKTA_MAX_PAGE_SIZE
                        else:
                            page_size = remaining_records
                        limit = f'&limit={page_size}'
                        next_response_wrapper = await self.api_client.get_search_results(query + limit, next_page_token)
                        next_response = json.loads(next_response_wrapper.read().decode('utf-8'))
                        if next_response_wrapper.code == 200:
                            data += next_response
                            next_page_token = Connector.verify_link_parameter(next_response_wrapper)
                            result_count += len(next_response)
                            local_result_count += len(next_response)
                        else:
                            return_obj = self.exception_response(next_response_wrapper.code,
                                                                 next_response.get('errorSummary'))
                            data = []
                            break
                    if data:
                        final_result = Connector.format_result(data)
                        if metadata:
                            return_obj['data'] = final_result if final_result else []
                        else:
                            return_obj['data'] = final_result[int(offset): total_records] if final_result else []
                        if next_page_token and result_count < self.api_client.result_limit:
                            return_obj['metadata'] = {"result_count": result_count,
                                                      "next_page_token": str(next_page_token)}
                    else:
                        if not return_obj.get('error') and return_obj.get('success') is not False:
                            return_obj['success'] = True
                            return_obj['data'] = []
                else:
                    return_obj = self.exception_response(response_wrapper.code, response_dict.get('errorSummary'))
            else:
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
            response_dict['message'] = str(ex)
            self.logger.error('error while fetching results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    @staticmethod
    def verify_link_parameter(response_wrapper):
        """
        verify if the headers is having link for next page
        :param response_wrapper, object
        :return: page token number, str
        """
        next_page_link = ""
        for link_key, link in response_wrapper.headers.items():
            if 'rel="next"' in link and link_key == 'Link':
                next_page_link = link
                break
        if not next_page_link:
            return None
        # if the after parameter is present at last of link parameter, angle index would be the end index.
        # if the after parameter is present in middle of link parameter, index of '&' would be the end index
        angle_index = next_page_link.find('>', next_page_link.find('after='))
        param_index = next_page_link.find('&', next_page_link.find('after='))
        if 0 < param_index < angle_index:
            end_index = param_index
        else:
            end_index = angle_index
        # filter the next page token
        next_page_token = next_page_link[(next_page_link.find('after=')):end_index]
        return next_page_token

    async def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.ping_data_source()
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
            response_dict['message'] = str(ex)
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

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
    def format_result(response):
        """
        formats the ip chain, domain and debug context response
        param: response, list
        """
        for event in response:
            ip_list = []
            # remove the client ip from request ipchain and retain ip address alone in request object inorder to handle
            # src-ip-ref in ibm-finding.
            if event.get('client', {}) and event['client'].get('ipAddress'):
                client_ip = event['client']['ipAddress']
            if event.get('request', {}) and event['request'].get('ipChain'):
                for ip_obj in event['request']['ipChain']:
                    if ip_obj.get('ip') != client_ip:
                        ip_list.append(ip_obj.get('ip'))
                if ip_list:
                    event['request']['ipChain'] = {'ip': ip_list}
                else:
                    del event['request']

            # As domain is referenced under extensions of autonomous system ,remove the invalid domain name
            # inorder to avoid the "null" reference when an invalid domain object is removed by stix shifter.
            if event.get('securityContext', {}) and event['securityContext'].get('domain'):
                if not Connector.DOMAIN_PATTERN.match(str(event['securityContext']['domain'])):
                    del event['securityContext']['domain']

            # wrap the debug context dict data under list, inorder to use groupReference in final stix, since
            # the reference is not working at high level key debugdata
            if event.get('debugContext', {}) and event['debugContext'].get('debugData', {}):
                event['debugContext'] = [event['debugContext']]

        return response
