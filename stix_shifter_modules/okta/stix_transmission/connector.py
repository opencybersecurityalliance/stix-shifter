from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json
from requests.exceptions import ConnectionError


class Connector(BaseSyncConnector):
    okta_max_page_size = 1000

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def create_results_connection(self, query, offset, length):
        """
        Fetching the results using query, offset and length
        :param query: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :return: return_obj, dict
        """
        return_obj = {}
        data = []
        result_count = 0
        response_dict = {}
        try:
            offset = int(offset)
            length = int(length)
            if isinstance(query, dict):
                query = json.dumps(query)
            limit = f'&limit={str(Connector.okta_max_page_size)}'
            response_wrapper = self.api_client.get_search_results(query + limit)
            response_dict = json.loads(response_wrapper.read().decode('utf-8'))

            if response_wrapper.code == 200:
                return_obj['success'] = True
                data += response_dict
                result_count += len(response_dict)
                after = Connector.verify_after_parameter(response_wrapper)
                # loop until if there is next page link and total records fetched is less than resultlimit
                while after and result_count < self.api_client.result_limit:
                    # if the after parameter is present at last of link parameter, angle index would be the end index.
                    # if the after parameter is present in middle of link parameter, index of '&' would be the end index
                    angle_index = after.find('>', after.find('after='))
                    param_index = after.find('&', after.find('after='))
                    if 0 < param_index < angle_index:
                        end_index = param_index
                    else:
                        end_index = angle_index
                    # filter the after parameter(next page number)
                    after_number = after[(after.find('after=')):end_index]
                    next_response_wrapper = self.api_client.get_search_results(query + limit + '&' + after_number)
                    next_response = json.loads(next_response_wrapper.read().decode('utf-8'))
                    if next_response_wrapper.code == 200:
                        data += next_response
                        after = Connector.verify_after_parameter(next_response_wrapper)
                        result_count += len(next_response)
                    else:
                        return_obj = self.exception_response(next_response_wrapper.code,
                                                             next_response.get('errorSummary'))
                        break
                return_obj['data'] = Connector.format_result(data)[offset:(offset + length)]
                # delete the error which occurred during pagination and return partial results
                if return_obj.get('success') is False and return_obj['data']:
                    return_obj['success'] = True
                    del return_obj['error'], return_obj['code']
            else:
                return_obj = self.exception_response(response_wrapper.code, response_dict.get('errorSummary'))

        except ConnectionError:
            response_dict['code'] = 300
            response_dict['message'] = 'Invalid host'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['message'] = str(ex)
            self.logger.error('error while fetching results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    @staticmethod
    def verify_after_parameter(response_wrapper):
        """
        verify if the headers is having link for next page
        :param response_wrapper, object
        :return: page token number, str
        """
        after_link = response_wrapper.headers['link'].split(",")
        after = ''.join([link for link in after_link if 'rel="next' in link])
        return after

    def ping_connection(self):
        """
        Ping the endpoint
        :return: return_object, dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = self.api_client.ping_data_source()
            response_code = response.response.status_code
            response_dict = json.loads(response.response.text)
            if response_code == 200:
                return_obj['success'] = True
            else:
                return_obj = self.exception_response(response_code, response_dict.get('errorSummary', ''))
        except ConnectionError:
            response_dict['code'] = 300
            response_dict['message'] = 'Invalid host'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['message'] = ex
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
        formats the ip chain response
        param: response, list
        """
        for event in response:
            ip_list = []
            # remove the client ip from request ipchain and retain ip address alone in request object inorder to handle
            # src-ip-ref in ibm-fidning.
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

        return response
