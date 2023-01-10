import json
import adal
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import copy


class Connector(BaseJsonSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.connector = __name__.split('.')[1]

        self.adal_response = Connector.generate_token(self, connection, configuration)
        if self.adal_response['success']:
            configuration['auth']['access_token'] = self.adal_response['access_token']
            self.api_client = APIClient(connection, configuration)
        else:
            self.init_error = True

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
            ErrorResponder.fill_error(return_obj, message=response_txt, connector=self.connector)
            raise Exception(return_obj)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'], connector=self.connector)
            raise Exception(return_obj)
        else:
            raise Exception(return_obj)

    async def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        if self.init_error:
            return self.adal_response
        response = await self.api_client.ping_box()
        response_code = response.code
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
        return return_obj

    async def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    async def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""

        response_txt = None
        return_obj = dict()

        try:
            if self.init_error:
                return self.adal_response
            response = await self.api_client.run_search(query, offset, length)
            return_obj = self._handle_errors(response, return_obj)
            response_json = json.loads(return_obj["data"])
            return_obj['data'] = response_json['Results']
            # Customizing the output json,
            # Get 'TableName' attribute from each row of event data
            # Create a dictionary with 'TableName' as key and other attributes in an event data as value
            # Filter the "None" and empty values except for RegistryValueName, which support empty string
            # Customizing of Registryvalues json
            table_event_data = []
            for event_data in return_obj['data']:
                lookup_table = event_data['TableName']
                event_data.pop('TableName')
                build_data = dict()
                build_data[lookup_table] = {k: v for k, v in event_data.items() if v or k == "RegistryValueName"}
                if lookup_table == "DeviceRegistryEvents":
                    registry_build_data = copy.deepcopy(build_data)
                    registry_build_data[lookup_table]["RegistryValues"] = []
                    registry_value_dict = {}
                    for k, v in build_data[lookup_table].items():
                        if k in ["RegistryValueData", "RegistryValueName", "RegistryValueType"]:
                            registry_value_dict.update({k: v})
                            registry_build_data[lookup_table].pop(k)
                    registry_build_data[lookup_table]["RegistryValues"].append(registry_value_dict)

                    build_data[lookup_table] = registry_build_data[lookup_table]
                build_data[lookup_table]['event_count'] = '1'
                table_event_data.append(build_data)
            return_obj['data'] = table_event_data
            return return_obj

        except Exception as ex:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception', connector=self.connector)
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise ex

    def generate_token(self, connection, configuration):
        """To generate the Token
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        return_obj = dict()

        authority_url = ('https://login.windows.net/' +
                         configuration['auth']['tenant'])
        resource = "https://" + str(connection.get('host'))

        try:
            context = adal.AuthenticationContext(
                authority_url, validate_authority=configuration['auth']['tenant'] != 'adfs',
            )
            response_dict = context.acquire_token_with_client_credentials(
                resource,
                configuration['auth']['clientId'],
                configuration['auth']['clientSecret'])

            return_obj['success'] = True
            return_obj['access_token'] = response_dict['accessToken']
        except Exception as ex:
            if ex.__class__.__name__ == 'AdalError':
                response_dict = ex.error_response
                ErrorResponder.fill_error(return_obj, response_dict, ['error_description'], connector=self.connector)
            else:
                ErrorResponder.fill_error(return_obj, message=str(ex), connector=self.connector)
            Connector.logger.error("Token generation Failed: " + str(ex.error_response))

        return return_obj
