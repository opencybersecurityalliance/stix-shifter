from ..base.base_results_connector import BaseResultsConnector
import json
from flatten_json import flatten
import copy
from .....utils.error_response import ErrorResponder
from os import path

MAX_LIMIT = 1000


class InvalidParameterException(Exception):
    pass


class AWSCloudWatchLogsResultsConnector(BaseResultsConnector):
    def __init__(self, client):
        self.client = client

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
            total_records = offset+length
            if total_records <= MAX_LIMIT:
                query['queryId'] = search_id
                response_dict = self.client.get_query_results(**query)
                return_obj['success'] = True
                results = response_dict['results'][offset:total_records]
                result_list = []
                guardduty_common_attr = ["account", "source", "detail_region", "detail_id",
                                         "detail_service_resourceRole", "detail_severity", "detail_type",
                                         "detail_createdAt", "detail_updatedAt", "detail_resource_resourceType",
                                         "detail_title", "detail_service_action_actionType",
                                         "detail_service_eventFirstSeen", "detail_service_eventLastSeen",
                                         "detail_service_archived", "detail_service_count", "detail_description",
                                         "detail_resource", "detail_service_eventFirstSeen",
                                         "detail_service_eventLastSeen"]
                self.format_results(guardduty_common_attr, result_list, results, return_obj)
            else:
                raise InvalidParameterException
        except Exception as ex:
            if isinstance(ex, InvalidParameterException):
                return_obj = dict()
                response_dict['__type'] = 'InvalidParameterException'
                response_dict['message'] = 'Total number of records (offset+length) must be less than or equal to 10000'
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            else:
                response_dict['__type'] = ex.__class__.__name__
                response_dict['message'] = ex
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
        return return_obj

    def format_results(self, guardduty_common_attr, result_list, results, return_obj):
        """
        Formatting the results
        :param guardduty_common_attr: list, list of guardduty common attributes
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
                guard_dict = dict()
                guard_dict['guardduty'] = dict()
                if flatten_results.get('detail_service_action_actionType') is None:
                    continue
                if flatten_results.get('detail_service_action_networkConnectionAction_protocol') == 'Unknown':
                    continue
                self.process_flatten_results(flatten_results, guard_dict, guardduty_common_attr, record_dict)
                result_list.append(guard_dict)
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

    def process_flatten_results(self, flatten_results, guard_dict, guardduty_common_attr, record_dict):
        """
        Processing the flatten results
        :param flatten_results: dict
        :param guard_dict: dict,
        :param guardduty_common_attr: list, list of guardduty common attributes
        :param record_dict: dict
        """
        guard_dict['guardduty'][flatten_results.get('detail_service_action_actionType')] = dict()
        for key, val in flatten_results.items():
            if val is None or val == []:
                continue
            elif val is False:
                val = str(val).lower()
            if key in guardduty_common_attr:
                guard_dict['guardduty'].update({key: val})
            elif 'detail_service_action_networkConnectionAction_protocol' in key:
                val = self.get_protocol(val)
                guard_dict['guardduty'][flatten_results['detail_service_action_actionType']].update({key: val})
            else:
                guard_dict['guardduty'][flatten_results['detail_service_action_actionType']].update({key: val})
        guard_dict['guardduty'].update({'@timestamp': record_dict['@timestamp']})
        guard_dict['guardduty'].update({'event_count': 1})

    @staticmethod
    def get_protocol(value):
        """
        Converting protocol number to name
        :param value: str, protocol
        :return: str, protocol
        """
        _json_path = path.abspath(path.join(path.dirname(__file__), '../../../..',
                                            'stix_translation/src/modules/aws_cloud_watch_logs/json'
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
