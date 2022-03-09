import json
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)
    PROVIDER = 'CrowdStrike'
    IDS_LIMIT = 500

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connector = __name__.split('.')[1]
        
        try:
            self.api_client = APIClient(connection, configuration)
            self.result_limit = Connector.get_result_limit(connection)

        except Exception as ex:
            self.init_error = ex

    def _handle_errors(self, response, return_obj):
        """Handling API error response
        :param response: response for the API
        :param return_obj: dict, response for the API call with status
        """
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['data'] = response_txt
            return return_obj
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt)
            raise Exception(return_obj)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    def ping_connection(self):
        response_txt = None
        return_obj = {}
        try:
            response = self.api_client.ping_box()
            response_code = response.code
            response_txt = response.read().decode('utf-8')
            if 199 < response_code < 300:
                return_obj['success'] = True
            elif isinstance(json.loads(response_txt), dict):
                response_error_ping = json.loads(response_txt)
                response_dict = response_error_ping['errors'][0]
                ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)
            else:
                raise Exception(response_txt)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
        
        return return_obj
            
    def send_info_request_and_handle_errors(self, ids_lst):
        return_obj = dict()
        response = self.api_client.get_detections_info(ids_lst)
        return_obj = self._handle_errors(response, return_obj)
        response_json = json.loads(return_obj["data"])
        return_obj['data'] = response_json['resources']

        return return_obj

    def handle_detection_info_request(self, ids):
        ids = [ids[x:x + self.IDS_LIMIT] for x in range(0, len(ids), self.IDS_LIMIT)]
        ids_lst = ids.pop(0)
        return_obj = self.send_info_request_and_handle_errors(ids_lst)

        for ids_lst in ids:
            curr_obj = self.send_info_request_and_handle_errors(ids_lst)
            return_obj['data'].extend(curr_obj['data'])

        return return_obj

    @staticmethod
    def get_result_limit(connection):
        default_result_limit = Connector.IDS_LIMIT
        if 'options' in connection:
            return connection['options'].get('result_limit', default_result_limit)
        return default_result_limit

    @staticmethod
    def _handle_quarantined_files(qua_files_lst, device_data):
        qua_files_event_lst = []
        if qua_files_lst:
            for file_dict in qua_files_lst:
                qua_file_data = dict()
                qua_file_data['display_name'] = file_dict['state']
                qua_file_data['quarantined_file_sha256'] = file_dict['sha256']
                qua_file_data['provider'] = Connector.PROVIDER
                qua_file_data.update(device_data)
                qua_files_event_lst.append(qua_file_data)

        return qua_files_event_lst

    @staticmethod
    def _handle_ioc(ioc_type, ioc_source, ioc_value):
        # ioc_value may contains many values separated by ','
        # first, we'll take the first value
        ioc_value = ioc_value.split(',')[0]  # TODO - handle the rest values
        ioc_data = dict()
        file_sources = ['file_read', 'file_write', 'library_load']
        # handle ioc_source = file_read / file_write
        if ioc_source and ioc_type and ioc_source in file_sources:
            if 'sha256' in ioc_type:
                ioc_data['sha256_ioc'] = ioc_value
            elif 'md5' in ioc_type:
                ioc_data['md5_ioc'] = ioc_value.replace("_", " ")
            ioc_data['display_name'] = ioc_source.replace("_", " ")

        # handle ioc_type = domain
        elif ioc_type and 'domain' in ioc_type:
            ioc_data['domain_ioc'] = ioc_value

        # handle ioc_type = 'registry_key'
        elif ioc_type and 'registry_key' in ioc_type:
            ioc_data['registry_key'] = ioc_value

        return ioc_data

    def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""
        result_limit = offset + length
        response_txt = None
        ids_obj = dict()
        return_obj = dict()
        table_event_data = []

        try:
            if self.init_error:
                raise self.init_error

            response = self.api_client.get_detections_IDs(query, result_limit)
            self._handle_errors(response, ids_obj)
            response_json = json.loads(ids_obj["data"])
            ids_obj['ids'] = response_json.get('resources')

            if ids_obj['ids']:  # There are not detections that match the filter arg
                return_obj = self.handle_detection_info_request(ids_obj['ids'])

                for event_data in return_obj['data']:
                    device_data = event_data['device']
                    hostinfo_data = event_data['hostinfo']
                    device_data.update(hostinfo_data)  # device & host
                    build_device_data = {k: v for k, v in device_data.items() if v}  # device & host
                    build_data = {k: v for k, v in event_data.items() if not isinstance(v, dict)
                                  and k not in 'behaviors'}  # other detection fields
                    build_data.update(build_device_data)
                    quarantined_files = event_data.get('quarantined_files')

                    if quarantined_files:
                        quarantined_files_lst = self._handle_quarantined_files(quarantined_files, build_data)
                        table_event_data.extend(quarantined_files_lst)
                    event_data.pop("quarantined_files", None)

                    for behavior in event_data['behaviors']:
                        ioc_type = behavior.pop("ioc_type", None)
                        ioc_source = behavior.pop("ioc_source", None)
                        ioc_value = behavior.pop("ioc_value", None)
                        ioc_data = self._handle_ioc(ioc_type, ioc_source, ioc_value)
                        build_ioc_data = {k: v for k, v in ioc_data.items() if v}
                        parent_details_data = behavior['parent_details']
                        build_event_data = {k: v for k, v in behavior.items() if v and not isinstance(v, dict)}
                        build_event_data.update(parent_details_data)
                        build_event_data.update(build_data)
                        build_event_data.update(build_ioc_data)
                        # build_event_data['device'] = build_device_data
                        build_event_data.pop('device_id')
                        build_event_data['provider'] = Connector.PROVIDER
                        build_event_data = {k: v for k, v in build_event_data.items() if v != "N/A"}
                        table_event_data.append(build_event_data)

            return_obj['data'] = table_event_data
            if not return_obj.get('success'):
                return_obj['success'] = True
            return return_obj

        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex
