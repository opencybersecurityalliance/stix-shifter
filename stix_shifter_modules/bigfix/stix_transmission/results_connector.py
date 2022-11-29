from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
import json
import time
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import xmltodict


class UnexpectedResponseException(Exception):
    pass


class ResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    @staticmethod
    def get_success_status(data_dict):
        items = ErrorResponder.get_struct_item(data_dict, ['results', '+isFailure=False'])
        return len(items) >= 0

    async def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = {}
        try:
            response = await self.api_client.get_search_results(search_id, offset, length)
            response_txt = response.read().decode('utf-8')
            response_code = response.code

            if 199 < response_code < 300:
                try:
                    response_dict = json.loads(response_txt)
                    return_obj['success'] = self.get_success_status(response_dict)
                    return_obj['data'] = []
                    for computer_obj in response_dict['results']:
                        is_failure = computer_obj['isFailure']
                        if not is_failure:
                            formatted_result_obj = self.format_computer_obj(computer_obj)
                            return_obj['data'].append(formatted_result_obj)
                except json.decoder.JSONDecodeError:
                    response_dict = xmltodict.parse(response_txt)
                    ErrorResponder.fill_error(return_obj, response_dict,
                                              ['BESAPI', 'ClientQueryResults', 'QueryResult', '+IsFailure=1',
                                               '~Result'], connector=self.connector)
            else:
                if ErrorResponder.is_plain_string(response_txt):
                    ErrorResponder.fill_error(return_obj, message=response_txt)
                else:
                    raise UnexpectedResponseException
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
        return return_obj

    @staticmethod
    def _format_socket_obj(obj_list, formatted_obj):
        """
        Function for formatting file object from API result
        :param obj_list: list, object attribute value list
        :param formatted_obj: dict
        :return: dict
        """
        attr_with_na_value_index_dict = {'local_address': (1, ('n/a',)), 'remote_address': (3, ('n/a',)),
                                         'local_port': (5, ('-1',)), 'remote_port': (7, ('-1',)),
                                         'sha256hash': (12, ('n/a',)), 'sha1hash': (14, ('n/a',)),
                                         'md5hash': (16, ('n/a',)), 'file_path': (17, ('n/a',)),
                                         'process_ppid': (18, ('n/a',)), 'process_user': (19, ('n/a',)),
                                         'timestamp': (21, ('0',)), 'process_name': (9, ('n/a',)),
                                         'process_id': (10, ('n/a', '0')), 'file_size': (20, ('0',))
                                         }
        for key, value in attr_with_na_value_index_dict.items():
            if obj_list[value[0]].strip() not in value[1]:
                formatted_obj[key] = obj_list[value[0]].strip()
        formatted_obj['type'] = "Socket"
        formatted_obj['protocol'] = 'tcp' if obj_list[22].strip() == 'True' else 'udp'
        formatted_obj['event_count'] = "1"
        return formatted_obj

    @staticmethod
    def _format_process_obj(obj_list, formatted_obj):
        """
        Function for formatting process object from API result
        :param obj_list: list, object attribute value list
        :param formatted_obj: dict
        :return: dict
        """
        attr_with_na_value_index_dict = {'sha256hash': (4, ('n/a',)), 'sha1hash': (6, ('n/a',)),
                                         'md5hash': (8, ('n/a',)), 'file_path': (9, ('n/a',)),
                                         'process_ppid': (10, ('n/a',)), 'process_user': (11, ('n/a',)),
                                         'timestamp': (13, ('0',)), 'process_name': (1, ('n/a',)),
                                         'process_id': (2, ('n/a', '0')), 'file_size': (12, ('0',))
                                         }
        for key, value in attr_with_na_value_index_dict.items():
            if obj_list[value[0]].strip() not in value[1]:
                formatted_obj[key] = obj_list[value[0]].strip()
        formatted_obj['type'] = obj_list[0].strip()
        formatted_obj['event_count'] = "1"
        return formatted_obj

    @staticmethod
    def _format_file_obj(obj_list, formatted_obj):
        """
        Function for formatting file object from API result
        :param obj_list: list, object attribute value list
        :param formatted_obj: dict
        :return: dict
        """
        attr_with_na_value_index_dict = {'sha256hash': (3, ('n/a',)), 'sha1hash': (5, ('n/a',)),
                                         'md5hash': (7, ('n/a',)), 'file_path': (8, ('n/a',)),
                                         'file_name': (1, ('n/a',)), 'file_size': (9, ('0',))
                                         }
        for key, value in attr_with_na_value_index_dict.items():
            if obj_list[value[0]].strip() not in value[1]:
                formatted_obj[key] = obj_list[value[0]].strip()
        formatted_obj['type'] = obj_list[0].strip()
        formatted_obj['timestamp'] = obj_list[10].strip()
        formatted_obj['event_count'] = "1"
        return formatted_obj

    @staticmethod
    def _format_adapter_obj(obj_list, formatted_obj):
        """
        Function for formatting adapter(mac address) object from API result
        :param obj_list: list, object attribute value list
        :param formatted_obj: dict
        :return: dict
        """
        attr_with_na_value_index_dict = {'mac': (2, ('n/a',))
                                         }
        for key, value in attr_with_na_value_index_dict.items():
            if obj_list[value[0]].strip() not in value[1]:
                if 'mac' in key:
                    formatted_obj[key] = obj_list[value[0]].strip().replace('-', ':')
                else:
                    formatted_obj[key] = obj_list[value[0]].strip()
        formatted_obj['type'] = obj_list[0].strip()
        formatted_obj['timestamp'] = int(time.time())
        formatted_obj['event_count'] = "1"
        return formatted_obj

    def format_computer_obj(self, computer_obj):
        # {"computerID": 12369754, "computerName": "bigdata4545.canlab.ibm.com", "subQueryID": 1,
        # "isFailure": false, "result": "file, .X0-lock,
        # sha256, 7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940,
        # sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb9a27af8597a1ddc51e89,
        # /tmp/.X0-lock, 1541424894", "ResponseTime": 0}
        result = computer_obj['result']
        obj_list = result.split(',')
        formatted_obj = {}
        computer_identity = str(computer_obj['computerID']) + '-' + computer_obj['computerName']
        formatted_obj['computer_identity'] = computer_identity
        formatted_obj['subQueryID'] = computer_obj['subQueryID']
        if result.startswith('process'):
            formatted_obj = self._format_process_obj(obj_list, formatted_obj)
        elif result.startswith('file'):
            formatted_obj = self._format_file_obj(obj_list, formatted_obj)
        elif result.lower().startswith('local'):
            formatted_obj = self._format_socket_obj(obj_list, formatted_obj)
        elif result.lower().startswith('address'):
            formatted_obj = self._format_adapter_obj(obj_list, formatted_obj)
        else:
            self.logger.debug('Unknown result')
        return formatted_obj
