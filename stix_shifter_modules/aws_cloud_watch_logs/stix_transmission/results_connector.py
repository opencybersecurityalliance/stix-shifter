import json
from flatten_json import flatten
import copy
from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json


class ResultsConnector(BaseResultsConnector):
    def __init__(self, client, options):
        self.client = client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.mapping_protocol = read_json('network_protocol_map', options)
        self.mapping_common_attr = read_json('common_attributes', options)

    async def create_results_connection(self, search_id, offset, length):
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

            response_dict = await self.client.makeRequest('logs', 'get_query_results', **query)
            return_obj['success'] = True
            results = response_dict['results'][offset:total_records]
            result_list = []
            self.format_results(result_list, results, return_obj)
        except Exception as ex:
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

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

    def get_protocol(self, value):
        """
        Converting protocol number to name
        :param value: str, protocol
        :return: str, protocol
        """
        if value.isdigit():
            for key, val in self.mapping_protocol.items():
                if val == value:
                    return key
        else:
            return value

    def get_guardduty_common_attr(self):
        """
        Fetching guardduty common attributes from common attributes json
        :return: list, guardduty common attributes
        """
        return self.mapping_common_attr.get('guardduty')
