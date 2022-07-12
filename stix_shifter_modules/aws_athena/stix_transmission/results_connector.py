import json
from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from flatten_json import flatten
from os import path
import os
import six
from collections.abc import Iterable


class AccessDeniedException(Exception):
    pass


class ResultsConnector(BaseResultsConnector):
    def __init__(self, client):
        self.client = client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

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
            offset = int(offset)
            length = int(length)
            total_records = offset+length
            search_id, service_type = search_id.split(':')[0], search_id.split(':')[1]
            if 'dummy' in search_id:
                return_obj = {'success': True, 'data': []}
                return return_obj

            result_response_list = await self.client.getPaginatedResult('athena', 'get_query_results', QueryExecutionId=search_id)
            
            # Formatting the response from api
            schema_columns = result_response_list[0]['Data']
            schema_columns = [list(x.values()) for x in schema_columns]
            schema_columns_list = [column_name for sublist in schema_columns for column_name in sublist]
            schema_row_values = result_response_list[1:]
            result_list = []
            for row in schema_row_values:
                row_values = [list('-') if list(x.values()) == [] else list(x.values()) for x in row['Data']]
                row_value_list = [row_value for sublist in row_values for row_value in sublist]
                response_dict = dict(zip(schema_columns_list, row_value_list))
                result_list.append(response_dict)
            results = result_list[offset:total_records]
            # Flattening the response
            flatten_result_cleansed = self.flatten_result(results, service_type)
            # Unflatten results using to_stix_map keys to avoid lengthy key value
            formatted_result = self.format_result(flatten_result_cleansed, service_type)
            return_obj['success'] = True
            return_obj['data'] = formatted_result

            # Delete output files(search_id.csv, search_id.csv.metadata) in s3 bucket
            get_query_response = await self.client.makeRequest('athena', 'get_query_execution', QueryExecutionId=search_id)
            s3_output_location = get_query_response['QueryExecution']['ResultConfiguration']['OutputLocation']
            s3_output_bucket_with_file = s3_output_location.split('//')[1]
            s3_output_bucket = s3_output_bucket_with_file.split('/')[0]
            s3_output_key = '/'.join(s3_output_bucket_with_file.split('/')[1:])
            s3_output_key_metadata = s3_output_key + '.metadata'
            delete = dict()
            delete['Objects'] = [{'Key': s3_output_key}, {'Key': s3_output_key_metadata}]
            # Api call to delete s3 object
            delete_object = await self.client.makeRequest('s3', 'delete_objects', Bucket=s3_output_bucket, Delete=delete)
            if delete_object.get('Errors'):
                message = delete_object.get('Errors')[0].get('Message')
                raise AccessDeniedException(message)
        except Exception as ex:
            return_obj = dict()
            response_dict['__type'] = ex.__class__.__name__
            response_dict['message'] = ex
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        self.logger.debug('Return Object: {}'.format(json.dumps(return_obj, indent=4)))
        return return_obj

    def flatten_result(self, results, service_type):
        """
        Flattening the result response
        :param results: list, results
        :return: list, flattened and empty values removed
        """
        flatten_results = []
        private_ip_address_key = 'resource#instancedetails#networkinterfaces#0#privateipaddress'
        action_type_key = 'service#action#actiontype'
        for obj in results:
            for key, value in obj.items():
                try:
                    obj[key] = json.loads(value)
                except ValueError:
                    pass
            flatten_obj = flatten(obj, '#')
            if service_type == 'vpcflow':
                flatten_obj.update({'name': 'VPC flow log'})
                temp = flatten_obj.get("action")
                flatten_obj["action"] = "network-traffic-" + temp.lower()
            if 'id' in flatten_obj:
                flatten_obj['finding_id'] = flatten_obj.pop('id')
            # Formatting to differentiate common key available in different action types for to STIX mapping
            if private_ip_address_key in flatten_obj and flatten_obj[action_type_key] == 'PORT_PROBE':
                flatten_obj['portprobe#'+private_ip_address_key] = flatten_obj.pop(private_ip_address_key)
            elif private_ip_address_key in flatten_obj and flatten_obj[action_type_key] == 'DNS_REQUEST':
                flatten_obj['dnsrequest#'+private_ip_address_key] = flatten_obj.pop(private_ip_address_key)
            flatten_results.append(flatten_obj)
        # Remove null values and empty objects from response
        flatten_result_cleansed = self.format_flatten_result(flatten_results)
        return flatten_result_cleansed

    def format_flatten_result(self, flatten_results):
        """
        Remove null values and empty objects from response
        :param flatten_results: list, flattened results
        :return: list, results with empty values removed
        """
        flatten_result_cleansed = []
        cleansed_obj = dict()
        purge_list = [[], {}, (), '', 'null', True, False, '-', None, 'Unknown']
        for obj in flatten_results:
            for key, value in obj.items():
                if value not in purge_list:
                    cleansed_obj[key] = value
                    if 'protocol' in key:
                        cleansed_obj[key] = self.get_protocol(value)
            cleansed_obj_copy = cleansed_obj.copy()
            flatten_result_cleansed.append(cleansed_obj_copy)
            cleansed_obj = dict()
        return flatten_result_cleansed

    def format_result(self, flatten_result_cleansed, service_type):
        """
        Unflattening the results using to_stix mapping keys
        :param flatten_result_cleansed: list, flattened results
        :param service_type: str, service name
        :return: list, formatted result
        """
        formatted_result = []
        transmit_basepath = os.path.abspath(__file__)
        translate_basepath = transmit_basepath.split(os.sep)[:-2]
        filepath = os.sep.join([*translate_basepath, "stix_translation", "json", 'to_stix_map.json'])
        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        map_data_keys = list(map_data[service_type].keys())
        ds_key_values = self.gen_dict_extract(key_to_search='ds_key', var=map_data)
        map_data_keys.extend(ds_key_values)
        flattened_obj = dict()
        obj_to_unflatten = dict()
        singular_obj = dict()
        service_log_dict = dict()
        for obj in flatten_result_cleansed:
            for key, value in obj.items():
                if key.replace('#', '_') in map_data_keys:
                    flattened_obj[key.replace('#', '_')] = value
                else:
                    if value not in flattened_obj.values():
                        obj_to_unflatten[key] = value
            unflatten_obj = self.unflatten(obj_to_unflatten, '#')
            flattened_obj.update(unflatten_obj)
            flattened_obj.update(singular_obj)
            service_log_dict = service_log_dict.copy()
            if flattened_obj:
                service_log_dict[service_type] = flattened_obj
                formatted_result.append(service_log_dict)
            flattened_obj = dict()
            obj_to_unflatten = dict()
        return formatted_result

    def gen_dict_extract(self, key_to_search, var):
        """
        Get nested data source keys in mapping file
        :param key_to_search: str, data source key
        :param var: dict, to stix mapping
        :return: object
        """
        if hasattr(var, 'items'):
            for k, v in var.items():
                if k == key_to_search:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key_to_search, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.gen_dict_extract(key_to_search, d):
                            yield result

    @staticmethod
    def get_protocol(value):
        """
        Converting protocol number to name
        :param key: str, data source key
        :param value: str, protocol
        :return: str, protocol
        """
        transmit_basepath = os.path.abspath(__file__)
        translate_basepath = transmit_basepath.split(os.sep)[:-2]
        _json_path = os.sep.join([*translate_basepath, "stix_translation", "json", "network_protocol_map.json"])

        if path.exists(_json_path):
            with open(_json_path) as f_obj:
                protocols = json.load(f_obj)
                if str(value).isdigit():
                    for key, val in protocols.items():
                        if val == str(value):
                            return key
                else:
                    return value
        else:
            raise FileNotFoundError

    @staticmethod
    def _unflatten_asserts(flat_dict, separator):
        assert isinstance(flat_dict, dict), "un_flatten requires dictionary input"
        assert isinstance(separator, six.string_types), "separator must be string"
        assert all((not value or not isinstance(value, Iterable) or
                    isinstance(value, six.string_types)
                    for value in flat_dict.values())), "provided dict is not flat"

    def unflatten(self, flat_dict, separator='_'):
        """
        Creates a hierarchical dictionary from a flattened dictionary
        Assumes no lists are present
        :param flat_dict: a dictionary with no hierarchy
        :param separator: a string that separates keys
        :return: a dictionary with hierarchy
        """
        self._unflatten_asserts(flat_dict, separator)
        # This global dictionary is mutated and returned
        unflattened_dict = dict()

        def _unflatten(dic, keys, value):
            for key in keys[:-1]:
                dic = dic.setdefault(key, {})
            dic[keys[-1]] = value
        list_keys = sorted(flat_dict.keys())
        for item in list_keys:
            _unflatten(unflattened_dict, item.split(separator),
                       flat_dict[item])
        return unflattened_dict
