import re
import json
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseJsonResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder


class ResultsConnector(BaseJsonResultsConnector):
    """ResultsConnector class"""
    def __init__(self, api_client):
        self.api_client = api_client
        self.connector = __name__.split('.')[1]

    async def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search_id, offset and length
        :param search_id:  Data Source search_id
        :param offset: Offset
        :param length: Length
        :return: dict
        """
        # Grab the response, extract the response code, and convert it to readable json
        return_obj = {}
        response_dict = {}
        try:
            response = await self.api_client.get_search_results(search_id, offset, length)
            response_code = response.code
            response_dict = json.load(response)
            response_text = response.content
            
            # Construct a response object
            return_obj = {}
            if response_code == 200:
                if "results" in response_dict:
                    results = response_dict['results']
                else:
                    results = []
                if results != []:
                    results = ResultsConnector.check_data(results)
                else:
                    results = []
                return_obj['success'] = True
                return_obj['data'] = results
            else:
                response_dict['type'] = str(response_code)
                if response_code == 404:
                    response_dict['type'] = "Unknown_sid"
                response_dict['message'] = response_text
                ErrorResponder.fill_error(return_obj, response_dict, ['messages'],
                                          connector=self.connector)
        except ClientConnectionError:
            response_dict['type'] = "ConnectionError"
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
        except TimeoutError as ex:
            response_dict['type'] = "Timeout"
            response_dict['messages'] = "TimeoutError"
            ErrorResponder.fill_error(return_obj, response_dict, ['messages'], connector=self.connector)
        except Exception as ex:
            if 'Authentication error' in str(ex):
                response_dict['type'] = "AuthenticationError"
            elif 'timeout_error' in str(ex):
                response_dict['type'] = "Timeout"
            response_dict['messages'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['messages'], connector=self.connector)

        return return_obj

    @staticmethod
    def check_data(res_data):
        """
        check data and update the api response as required
        :param item: list of dictionary items
        :return: list
        """
        for item in res_data:
            # check if value is '-', set it None
            for key, value in item.items():
                if item.get(key) is not None and value == "-":
                    item[key] = None
            # set name and query count None as query (dns) is none
            if item.get("query") is None:
                item["name"] = None
                item["query_count"] = None
                item["query_type"] = None
            # create custom network data
            if (item.get("src_ip") is not None or item.get("src_port") is not None) and (
                    item.get("dest_port") is not None or item.get("dest_ip") is not None):
                item["networkdata"] = ResultsConnector.network_traffic_check(item)

            # set subject as None if it is not an email event
            if (item.get("subject") is not None and item.get("recipient") is None):
                item["subject"] = None
            # set process_exec as none if process_name and process_exec are same
            ResultsConnector.process_data_check(item)

            # check email data
            ResultsConnector.email_data_check(item)

            # add mime_type_raw for artifact object
            ResultsConnector.artifact_data(item)

            # if file name is none set file_hash also none
            if item.get("file_name") is None:
                item["file_hash"] = None
            
            # create registry value as dictionary object
            if item.get("registry_value_name") is not None:
                item["registry_value"] = ResultsConnector.registry_value_check(item)

            # ibm finding object change for alert
            if item.get("severity") is not None:
                if item.get("type") is not None and item.get("type") == "alert":
                    ResultsConnector.alert_check_ibm_finding(item)

            # extracts SHA1,SHA256 and MD5 values from file_hash
            item["file_hashes"] = ResultsConnector.filehash_check(item)

        return res_data

    @staticmethod
    def artifact_data(item_in):
        if item_in.get('_raw'):
            item_in['mime_type_raw'] = 'text/plain'

    @staticmethod
    def process_data_check(item_in):
        """check process data"""
        if (item_in.get("process_name") is not None and item_in.get("process_exec") is not None):
            if item_in["process_name"] == item_in["process_exec"]:
                item_in["process_exec"] = None
        if (item_in.get("parent_process_name") is not None and item_in.get("parent_process_exec") is not None):
            if item_in["parent_process_name"] == item_in["parent_process_exec"]:
                item_in["parent_process_exec"] = None

    @staticmethod
    def email_data_check(item_in):
        """check email data and set is_multipart required field"""
        if item_in.get("src_user") is not None and item_in.get("src_user_domain") is None:
            item_in["src_user"] = None
        # set is_multipart with false as default if there is email message property
        if (item_in.get("subject") is not None or item_in.get("recipient") is not None or item_in.get(
                "src_user") is not None) and item_in.get("is_multipart") is None:
            item_in["is_multipart"] = False

    @staticmethod
    def registry_value_check(item_in):
        """check and create valid network traffic event data"""
        registry_value_dict = {}
        registry_value_dict.update({"registryValueName": item_in["registry_value_name"]})
        if item_in.get("registry_value_data") is not None:
            registry_value_dict.update({"registryValueData": item_in["registry_value_data"]})
        return registry_value_dict

    @staticmethod
    def alert_check_ibm_finding(item_in):
        """check alert event and create custom field"""
        item_in["finding_type"] = item_in.get("type")
        item_in["alert_severity"] = item_in.get("severity")
        item_in["alert_signature"] = item_in.get("signature")
        item_in["alert_id"] = item_in.get("id")
        item_in["alert_description"] = item_in.get("description")
        item_in["severity"] = None

    @staticmethod
    def network_traffic_check(item_in):
        """check and create valid network traffic event data"""

        # set dest as None if it is same as dest_ip
        if item_in.get("dest_ip") is not None and item_in.get("dest") is not None:
            if item_in["dest_ip"] == item_in["dest"]:
                item_in["dest"] = None
        # set src as None if it is same as src_ip
        if item_in.get("src_ip") is not None and item_in.get("src") is not None:
            if item_in["src_ip"] == item_in["src"]:
                item_in["src"] = None

        network_dict = {}
        if item_in.get("src_port") is not None:
            network_dict.update({"src_port": item_in["src_port"]})
            item_in["src_port"] = None
        if item_in.get("dest_port") is not None:
            network_dict.update({"dest_port": item_in["dest_port"]})
            item_in["dest_port"] = None
        if item_in.get("protocol") is None and item_in.get("transport") is None:
            network_dict.update({"protocol": "tcp"})
        if item_in.get("protocol") is not None:
            network_dict.update({"protocol": item_in["protocol"]})
        if item_in.get("transport") is not None:
            network_dict.update({"transport": item_in["transport"]})
        if item_in.get("direction") is not None:
            network_dict.update({"direction": item_in["direction"]})

        return network_dict

    @staticmethod
    def filehash_check(item_in):
        """file_hash value check"""
        hashdict = {}
        if item_in.get('file_hash') is not None and ',' in item_in.get('file_hash'):
            values = item_in.get('file_hash').split(',')
            del item_in["file_hash"]
            for value in values:
                if 'SHA1' in value:
                    hashdict.update({"file_sha1": value.split('=')[1]})
                elif 'SHA256' in value:
                    hashdict.update({"file_sha256": value.split('=')[1]})
                elif 'MD5' in value:
                    hashdict.update({"file_md5": value.split('=')[1]})
        elif item_in.get('file_hash') is not None:
            if re.compile("^[a-f0-9]{32}$").match(item_in["file_hash"]) is not None:
                hashdict.update({"file_md5": item_in['file_hash']})
            elif re.compile(r'\b[0-9a-f]{40}\b').match(item_in["file_hash"]) is not None:
                hashdict.update({"file_sha1": item_in['file_hash']})
            elif re.compile("[A-Fa-f0-9]{64}").match(item_in["file_hash"]) is not None:
                hashdict.update({"file_sha256": item_in['file_hash']})
            else:
                hashdict.update({"unknown": item_in['file_hash']})
            del item_in['file_hash']

        return hashdict
