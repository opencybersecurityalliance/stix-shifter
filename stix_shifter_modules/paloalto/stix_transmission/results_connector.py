from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from aiohttp.client_exceptions import ClientConnectionError
from .response_mapper import ResponseMapper
from os import path

TO_STIX_PATH = "../stix_translation/json/to_stix_map.json"
CONFIG_MAP_PATH = "../stix_translation/json/config_map.json"


class FileNotFoundException(Exception):
    pass


class InvalidQueryException(Exception):
    pass


class ResultsConnector(BaseResultsConnector):

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    @staticmethod
    def load_json(rel_path_of_file):
        """
        Consumes a json file and returns a dictionary
        :param rel_path_of_file: str
        :return: dict
        """
        _json_path = path.dirname(path.realpath(__file__)) + "/" + rel_path_of_file
        try:
            if path.exists(_json_path):
                with open(_json_path, encoding='utf-8') as f_obj:
                    return json.load(f_obj)
            raise FileNotFoundException
        except FileNotFoundException as e:
            raise FileNotFoundError(f'{rel_path_of_file} not found') from e

    async def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search id, offset and length
        :param search_id: str, search id generated in transmit query
        :param offset: str, offset value
        :param length: str, length value
        :return: dict
        """
        response_dict = {}
        return_obj = {}
        results = []
        response_wrapper = None
        to_stix_mapping = ResultsConnector.load_json(TO_STIX_PATH)
        mandatory_map = ResultsConnector.load_json(CONFIG_MAP_PATH)["mandatory_properties_to_stix"]
        try:
            min_range = int(offset)
            max_range = int(offset) + int(length)
            # Grab the response, extract the response code, and convert it to readable json
            response_wrapper = await self.api_client.get_search_results(search_id)
            response_text = json.loads(response_wrapper.read().decode('utf-8'))
            if response_wrapper.code != 200:
                return_obj = ResponseMapper().status_code_mapping(response_wrapper.code, response_text)
            else:
                if 'status' in response_text['reply'].keys() and response_text['reply']['status'] \
                        in ('SUCCESS', 'PARTIAL_SUCCESS'):
                    if 'data' in response_text['reply']['results'].keys() and \
                            response_text['reply']['number_of_results'] > 0:
                        results = ResultsConnector.format_results_data(
                            response_text['reply']['results']['data'], to_stix_mapping, mandatory_map)
                    elif 'stream_id' in response_text['reply']['results'].keys():
                        stream_wrapper = await self.api_client.get_stream_results(
                            response_text['reply']['results']['stream_id'])
                        if stream_wrapper.code != 200:
                            return_obj = ResponseMapper().status_code_mapping(stream_wrapper.code,
                                                                              stream_wrapper.read().decode('utf-8'))
                        else:
                            results = ResultsConnector.format_stream_data(stream_wrapper.read().decode('utf-8'),
                                                                          to_stix_mapping, mandatory_map)
                    return_obj['success'] = True
                    return_obj['data'] = results[min_range:max_range] if results else []

                elif 'status' in response_text['reply'].keys() and response_text['reply']['status'] == 'FAIL':
                    raise InvalidQueryException

        except ValueError as ex:
            if response_wrapper is not None:
                self.logger.debug(response_wrapper.read())
            raise Exception(f'Cannot parse response: {ex}') from ex
        except InvalidQueryException:
            response_dict['type'] = "SyntaxError"
            response_dict['message'] = 'Tenant Query Failed'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        except Exception as ex:
            if 'timeout_error' in str(ex):
                response_dict['type'] = 'TimeoutError'
            else:
                response_dict['type'] = ex.__class__.__name__
            response_dict['message'] = ex
            self.logger.error('error when getting search results: %s', ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.api_client.connector)
        return return_obj

    @staticmethod
    def format_results_data(result_data, to_stix_mapping, mandatory_map):
        """
        Format the results in json format
        :param result_data: list of dictionary items
        :param to_stix_mapping: to stix mapping dictionary
        :param mandatory_map: dictionary
        :return: list
        """
        results = []
        dataset_map = result_data[0]['dataset_name']
        try:
            for log in result_data:
                data = {}
                results_dict = {}
                dataset = ""
                for field, value in log.items():
                    if value is not None and value != "NULL" and value != '' and field != 'dataset_name' \
                            and (field in to_stix_mapping[dataset_map].keys()):
                        stix_data_map = to_stix_mapping[dataset_map][field]
                        data = ResultsConnector.check_object(stix_data_map, mandatory_map, data, log,
                                                             field, value)
                    elif field == 'dataset_name':
                        dataset = value

                results_dict[dataset] = data
                results.append(results_dict)
        except (KeyError, IndexError, TypeError) as e:
            raise e
        return results

    @staticmethod
    def format_stream_data(stream_data, to_stix_mapping, mandatory_map):
        """
        Format the stream data into json format
        :param stream_data: string
        :param to_stix_mapping: to stix mapping dictionary
        :param mandatory_map: dictionary
        :return: list
        """
        results = []
        try:
            temp_data = stream_data.split("\n")
            dataset_map = json.loads(temp_data[0])['dataset_name']
            for log in temp_data:
                if log > " ":
                    data = {}
                    results_dict = {}
                    dataset = ""
                    log_dict = json.loads(log)
                    for field, value in log_dict.items():
                        if value is not None and value != "NULL" and value != '' and field != 'dataset_name' \
                                and (field in to_stix_mapping[dataset_map].keys()):
                            stix_data_map = to_stix_mapping[dataset_map][field]
                            data = ResultsConnector.check_object(stix_data_map, mandatory_map,
                                                                 data, log_dict, field, value)
                        elif field == 'dataset_name':
                            dataset = value
                    results_dict[dataset] = data
                    results.append(results_dict)
        except (KeyError, IndexError, TypeError) as e:
            raise e
        return results

    @staticmethod
    def check_object(stix_data_map, mandatory_map, data, log, field, value):
        """
        The mandatory stix fields are removed, if no value is received from data source
        :param stix_data_map: list of dictionary items
        :param mandatory_map : list of dictionary items
        :param data : dictionary
        :param log: dictionary
        :param field : string
        :param value: string/integer
        :return: list of dictionary items
        """
        try:

            if isinstance(stix_data_map, list):
                obj_list = [obj["object"] for obj in stix_data_map if "object" in obj.keys()]
                for obj in obj_list:
                    if obj in mandatory_map.keys():
                        data = ResultsConnector.check_mandatory_map(mandatory_map, obj, log, data, field, value)
                    else:
                        # Since these ip addresses may receive a single ip or list of ips, they are sent as list value
                        # for the to_stix conversion
                        data[field] = value.split(",") if field in ["agent_ip_addresses", "agent_ip_addresses_v6",
                                                                    "dst_agent_ip_addresses_v6"] else value

            elif isinstance(stix_data_map, dict):
                if stix_data_map["object"] in mandatory_map.keys():
                    data = ResultsConnector.check_mandatory_map(mandatory_map, stix_data_map["object"],
                                                                log, data, field, value)
                else:

                    data[field] = value

        except (KeyError, IndexError, TypeError) as e:
            raise e
        return data

    @staticmethod
    def check_mandatory_map(mandatory_map, obj, log, data, field, value):
        """
        Donot add the the fields which belongs to the object of mandatory field ,
        if data source doesnt return any value if the mandatory field
        :param mandatory_map: list of dictionary items
        :param obj : string
        :param log : dictionary
        :param data :  dictionary
        :param field : string
        :param value : string/integer
        """
        try:
            if "file" in obj:
                if mandatory_map[obj][0] in log.keys() and log[mandatory_map[obj][0]] != "NULL" and \
                        log[mandatory_map[obj][0]] != '' and \
                        log[mandatory_map[obj][0]] is not None:
                    data[field] = value
            elif obj in ["user", "nt"]:
                if obj == "nt":
                    data = ResultsConnector.process_nt_obj(mandatory_map, obj, data, log, value, field)
                else:
                    if any((item in log.keys() and log[item] != "NULL" and log[item] != '' and log[item] is not None)
                           for item in mandatory_map[obj]):
                        data[field] = value
        except (KeyError, IndexError, TypeError) as e:
            raise e
        return data

    @staticmethod
    def process_nt_obj(mandatory_map, obj, data, log, value, field):
        """
        check if any of the fields in the list is not null
        :param mandatory_map: list of dictionary items
        :param obj : string
        :param log : dictionary
        :param data :  dictionary
        :param field : string
        :param value : string/integer
        """
        nt_obj = False
        try:
            for i in mandatory_map[obj]:
                if isinstance(i, list):
                    if any((item in log.keys() and log[item] != "NULL" and log[item] != '' and log[item] is not None)
                            for item in i):
                        nt_obj = True
                else:
                    if nt_obj:
                        data[i] = log[i] if (log[i] != "NULL" and log[i] != '' and log[i] is not None) else "NULL"
                        data[field] = value

        except (KeyError, IndexError, TypeError) as e:
            raise e
        return data
