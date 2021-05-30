import json
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy


class Connector(BaseSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)
    PROVIDER = 'CrowdStrike'

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        try:
            self.api_client = APIClient(connection, configuration)

        except Exception as ex:
            self.init_error = ex

    @staticmethod
    def _handle_errors(response, return_obj):
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
            ErrorResponder.fill_error(return_obj, response_json, ['reason'])
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""

        response_txt = None
        ids_obj = dict()
        return_obj = dict()
        table_event_data = []

        try:
            if self.init_error:
                raise self.init_error
            for q in query:
                response = self.api_client.get_detections_IDs(q)
                print(response)
                self._handle_errors(response, ids_obj)
                response_json = json.loads(ids_obj["data"])
                ids_obj['ids'] = response_json['resources']

                if not ids_obj['ids']:  # There are not detections that match the filter arg
                    continue

                response = self.api_client.get_detections_info(ids_obj['ids'])
                print(response)
                return_obj = self._handle_errors(response, return_obj)
                response_json = json.loads(return_obj["data"])
                return_obj['data'] = response_json['resources']

                for event_data in return_obj['data']:
                    device_data = event_data['device']
                    hostinfo_date = event_data['hostinfo']
                    device_data.update(hostinfo_date)  # device & host
                    build_device_data = {k: v for k, v in device_data.items() if v}  # device & host
                    build_data = {k: v for k, v in event_data.items() if not isinstance(v, dict)
                                  and k not in 'behaviors'}  # other detection fields
                    build_data.update(build_device_data)

                    for behavior in event_data['behaviors']:
                        parent_details_data = behavior['parent_details']
                        build_event_data = {k: v for k, v in behavior.items() if v and not isinstance(v, dict)}
                        build_event_data.update(parent_details_data)
                        build_event_data.update(build_data)
                        #build_event_data['device'] = build_device_data
                        build_event_data.pop('device_id')
                        build_event_data['provider'] = Connector.PROVIDER
                        table_event_data.append(build_event_data)

            return_obj['data'] = table_event_data
            return return_obj

            # Customizing the output json,
            # Get 'TableName' attribute from each row of event data
            # Create a dictionary with 'TableName' as key and other attributes in an event data as value
            # Filter the "None" and empty values except for RegistryValueName, which support empty string
            # Customizing of Registryvalues json

        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex
