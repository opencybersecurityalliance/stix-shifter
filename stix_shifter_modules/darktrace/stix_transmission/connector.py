from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from .api_client import APIClient
import json
from os import path
from requests.exceptions import ConnectionError

CONFIG_MAP_PATH = "../stix_translation/json/config_map.json"


class InvalidRequestException(Exception):
    pass


class InternalServerErrorException(Exception):
    pass


class InvalidArguments(Exception):
    pass


class InvalidAuthenticationException(Exception):
    pass


class Connector(BaseSyncConnector):

    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.config_map = self.load_json(CONFIG_MAP_PATH)
        self.connector = __name__.split('.')[1]

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        if path.exists(_json_path):
            with open(_json_path, encoding='utf-8') as f_obj:
                return json.load(f_obj)
        raise FileNotFoundError

    def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search_id, offset and length
        :param search_id: str, Data Source query
        :param offset: str, Offset value
        :param length: str, Length value
        :return: dict
        """
        return_obj = {}
        response_dict = {}

        try:
            offset = int(offset)
            length = int(length)

            if isinstance(search_id, dict):
                search_id = json.dumps(search_id)

            response_wrapper = self.api_client.get_search_results(search_id)

            if response_wrapper.code == 200:
                return_obj['success'] = True
            # Both InvalidAuthentication and InvalidRequest returns the same error code 400.
            # Verifying the error message to identify InvalidAuthentication error.
            elif response_wrapper.code == 400 and 'API SIGNATURE ERROR' in response_wrapper.response.text:
                raise InvalidAuthenticationException
            elif response_wrapper.code == 408:
                raise TimeoutError(response_wrapper.response.text)
            elif 399 < response_wrapper.code < 500:
                raise InvalidRequestException(response_wrapper.response.text)
            elif response_wrapper.code == 500:
                raise InternalServerErrorException(response_wrapper.response.text)

            response_dict = json.loads(response_wrapper.read().decode('utf-8'))

            if response_dict.get('error'):
                raise InvalidArguments(response_dict['error'])

            results = self.get_results_data(response_dict)
            return_obj['data'] = results[offset:length]
            return_obj = self.check_empty_data(return_obj)

        except InvalidArguments as ex:
            response_dict['code'] = 1002
            response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except InvalidAuthenticationException:
            response_dict['code'] = 1001
            response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ConnectionError:
            response_dict['code'] = 1003
            response_dict['message'] = "Invalid Host/Port"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except TimeoutError as ex:
            response_dict['code'] = 1004
            response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except InvalidRequestException as ex:
            response_dict['code'] = 1005
            response_dict['message'] = 'Bad Request' if 'Bad request' in str(ex) else str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj

    def get_results_data(self, response_dict):

        proto_field = {"dhcp": "udp", "x509": "ssl", "files_identified": "tcp", "software": "tcp",
                       "device_details": "udp"}

        results = []
        for log in response_dict['hits']['hits']:
            if log['_source']['@type'] in self.config_map['DT_Protocols']:
                element_dict = {}

                if log['_source']['@type'] != 'conn':
                    data = {}
                    for key, value in log['_source']['@fields'].items():
                        if key in self.config_map['DT_NetworkTraffic']:
                            data[key] = value

                    if 'proto' not in data.keys():
                        data['proto'] = proto_field.get(log['_source']['@type'], log['_source']['@type'])
                    element_dict['conn'] = data
                element_dict[log['_source']['@type']] = log['_source']['@fields']
                results.append(element_dict)

        return results

    @staticmethod
    def check_empty_data(response):
        """
        Adding protocol, file name value and remove empty data
        params: res_dict(dict) response dictionary
        return: res_dict(dict)
        """

        file_fields = ["filename", "sha1_file_hash", "sha1", "md5_file_hash", "md5", "sha256_file_hash", "sha256",
                       "mime", "file_mime_type", "mime_type", "dcc_mime_type", "total_bytes", "file_msg", "read_size",
                       "write_size", "dcc_file_size"]

        for index in range(len(response['data'])):
            for key in response['data'][index]:
                if response['data'][index][key].get("filename") is None:
                    if response['data'][index][key].keys() & file_fields:
                        response['data'][index][key]["filename"] = "null"

        return response

    def ping_connection(self):
        """
        Ping the endpoint
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        try:
            response = self.api_client.ping_box()
            response_code = response.response.status_code
            response_dict = json.loads(response.response.text)

            if response_code == 200:  # and response_dict['status'] == 'SUCCESS':
                return_obj['success'] = True
            elif response_code == 400:
                raise InvalidAuthenticationException

            if response_dict.get('error'):
                raise InvalidArguments(response_dict['error'])

        except InvalidArguments as ex:
            response_dict['type'] = 1002
            response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except InvalidAuthenticationException:
            response_dict['code'] = 1001
            response_dict['message'] = "Invalid Authentication"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except ConnectionError:
            response_dict['code'] = 1003
            response_dict['message'] = "Invalid Host/Port"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except Exception as ex:
            response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error while pinging: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        return return_obj
