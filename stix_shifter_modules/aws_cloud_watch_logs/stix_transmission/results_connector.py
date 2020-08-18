import json
from flatten_json import flatten
import copy
from os import path
from importlib import import_module
from pathlib import Path

from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class ResultsConnector(BaseResultsConnector):
    def __init__(self, client):
        self.client = client
        self.logger = logger.set_logger(__name__)

    def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search id, offset and length
        :param search_id: str, search id generated in transmit query
        :param offset: str, offset value
        :param length: str, length value
        :return: dict
        """
        return_obj = dict()
        response_dict = dict()
        try:
            query = dict()
            offset = int(offset)
            length = int(length)
            if ':' in search_id:
                search_id = search_id.split(':')[0]
            total_records = offset+length
            query['queryId'] = search_id
            response_dict = self.client.get_query_results(**query)
            return_obj['success'] = True
            results = response_dict['results'][offset:total_records]
            result_list = []
            self.format_results(result_list, results, return_obj)
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        self.logger.debug('Return Object: {}'.format(json.dumps(return_obj, indent=4)))
        return return_obj

    def format_results(self, result_list, results, return_obj):
        """
        Formatting the results
        :param result_list: list
        :param results: list, results
        :param return_obj: dict
        :return: dict
        """
        for record in results:
            record_dict = dict()
            for data in record:
                record_dict[data['field']] = data['value']
            if 'source' in record_dict.keys() and record_dict['source'] == 'aws.guardduty':
                json_message = record_dict['@message']
                data = json.loads(json_message)
                flatten_results = flatten(data)
                flatten_results = {k: v for k, v in flatten_results.items() if v != "" and v != {}}
                if flatten_results.get('detail_service_action_actionType') is None:
                    continue
                if flatten_results.get('detail_service_action_networkConnectionAction_protocol') == 'Unknown':
                    continue
                guardduty_results = self.process_flatten_guardduty_results(flatten_results)
                guardduty_results['guardduty'].update({'@timestamp': record_dict['@timestamp']})
                guardduty_results['guardduty'].update({'event_count': 1})
                result_list.append(guardduty_results)
            elif 'source' not in record_dict.keys():
                vpc_dict = dict()
                vpc_dict['vpcflow'] = copy.deepcopy(record_dict)
                vpc_dict['vpcflow']['protocol'] = self.get_protocol(vpc_dict['vpcflow']['protocol'])
                vpc_dict['vpcflow']['event_count'] = 1
                result_list.append(vpc_dict)
            else:
                json_message = record_dict['@message']
                data = json.loads(json_message)
                flatten_results = flatten(data)
                result_list.append(flatten_results)

        return_obj['data'] = result_list

    def process_flatten_guardduty_results(self, flatten_results):
        """
        Processing the flatten results
        :param flatten_results: dict
        :return: dict
        """
        guard_dict, guard_dict['guardduty'], guard_dict['guardduty'][flatten_results.get(
            'detail_service_action_actionType')] = dict(), dict(), dict()
        guardduty_common_attr = self.get_guardduty_common_attr()
        for key, val in flatten_results.items():
            if val is None or val == []:
                continue
            elif val is False or val is True:
                val = str(val).lower()
            if key in guardduty_common_attr:
                guard_dict['guardduty'].update({key: val})
            elif 'detail_service_action_networkConnectionAction_protocol' in key:
                val = self.get_protocol(val)
                guard_dict['guardduty'][flatten_results['detail_service_action_actionType']].update({key: val})
            else:
                guard_dict['guardduty'][flatten_results['detail_service_action_actionType']].update({key: val})
        return guard_dict

    @staticmethod
    def get_protocol(value):
        """
        Converting protocol number to name
        :param value: str, protocol
        :return: str, protocol
        """
        modules = import_module('stix_shifter_modules')
        if '__file__' in dir(modules):
            modules_path = Path(modules.__file__).parent
        else:
            modules_path = modules.__path__._path[0]
        _json_path = path.abspath(path.join(modules_path,
                                            'aws_cloud_watch_logs/stix_translation/json'
                                            '/network_protocol_map.json'))
        if path.exists(_json_path):
            with open(_json_path) as f_obj:
                protocols = json.load(f_obj)
                if value.isdigit():
                    for key, val in protocols.items():
                        if val == value:
                            return key
                else:
                    return value
        else:
            raise FileNotFoundError

    @staticmethod
    def get_guardduty_common_attr():
        """
        Fetching guardduty common attributes from common attributes json
        :return: list, guardduty common attributes
        """
        modules = import_module('stix_shifter_modules')
        if '__file__' in dir(modules):
            modules_path = Path(modules.__file__).parent
        else:
            modules_path = modules.__path__._path[0]
        _json_path = path.abspath(path.join(modules_path,
                                            'aws_cloud_watch_logs/stix_translation/json'
                                            '/common_attributes.json'))
        if path.exists(_json_path):
            with open(_json_path) as f_obj:
                common_attr_dict = json.load(f_obj)
                common_attr_list = common_attr_dict.get('guardduty')
                return common_attr_list
        else:
            raise FileNotFoundError
