import json
import adal
import re
from flatten_json import flatten
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseSyncConnector):
    init_error = None
    max_limit = 1000

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.adal_response = Connector.generate_token(connection, configuration)
        if self.adal_response['success']:
            configuration['auth']['access_token'] = self.adal_response['access_token']
            self.api_client = APIClient(connection, configuration)
        else:
            self.init_error = True


    def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        if self.init_error:
            self.logger.error("Token Generation Failed:")
            return self.adal_response
        response = self.api_client.ping_box()
        response_code = response.code
        response_dict = json.loads(response.read())
        if 200 <= response_code < 300:
            return_obj['success'] = True
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'])
        return return_obj

    def delete_query_connection(self, search_id):
        """"delete_query_connection response
        :param search_id: str, search_id"""
        return {"success": True, "search_id": search_id}

    def create_results_connection(self, query, offset, length):
        """"built the response object
        :param query: str, search_id
        :param offset: int,offset value
        :param length: int,length value"""
        response = None
        response_dict = dict()
        return_obj = dict()
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length

        try:
            if self.init_error:
                self.logger.error("Token Generation Failed:")
                return self.adal_response
            # check for length value against the max limit(1000) of $top param in data source
            if length <= self.max_limit:
                # $skip(offset) param not included as data source provides incorrect results for some of the queries
                response = self.api_client.run_search(query, total_records)
            elif length > self.max_limit:
                response = self.api_client.run_search(query, self.max_limit)
            response_code = response.code
            response_dict = json.loads(response.read())
            if 199 < response_code < 300:
                return_obj['success'] = True
                return_obj['data'] = response_dict['value']
                while len(return_obj['data']) < total_records:
                    try:
                        next_page_link = response_dict['@odata.nextLink']
                        response = self.api_client.next_page_run_search(next_page_link)
                        response_code = response.code
                        response_dict = json.loads(response.read())
                        if 199 < response_code < 300:
                            return_obj['data'].extend(response_dict['value'])
                        else:
                            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'])
                    except KeyError:
                        break
                # slice the cumulative records as per the provided offset and length(limit)
                return_obj['data'] = return_obj['data'][offset:total_records]

                single_level_json = []
                # flatten result json to single level
                for node in return_obj['data']:

                    # new code
                    if len(node['processes']) > 1:
                        del node['fileStates']

                    # customize results for fileHashes
                    if 'fileStates' in node:
                        for file in node["fileStates"]:
                            if file["fileHash"] is not None:
                                file[file["fileHash"]['hashType']] = file["fileHash"]['hashValue']

                    if 'processes' in node:
                        for process in node["processes"]:
                            if process["fileHash"] is not None:
                                process[process["fileHash"]['hashType']] = process["fileHash"]['hashValue']

                    # pass the alert nodes for JSON flattening
                    flat_json = Connector.flatten_json(node)
                    # extract and replace valid IP values
                    for key in list(flat_json):
                        # check for string attributes to extract IP value
                        if flat_json[key] is not None and isinstance(flat_json[key], str):
                            ip_value = re.findall(r'[0-9]+(?:\.[0-9]+){3}', flat_json[key])
                            if ip_value:
                                flat_json[key] = ip_value[0]
                        # check for removing keys (none and bool type)
                        elif flat_json[key] is None or isinstance(flat_json[key], bool):
                            flat_json.pop(key)
                    single_level_json.append(flat_json)

                return_obj['data'] = single_level_json

            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'])

        except Exception as ex:
            if response_dict is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_dict))
            else:
                raise ex
        return return_obj

    @staticmethod
    def generate_token(connection, configuration):
        """To generate the Token
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        return_obj = dict()

        authority_url = ('https://login.microsoftonline.com/' +
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
                ErrorResponder.fill_error(return_obj, response_dict, ['error_description'])
            else:
                ErrorResponder.fill_error(return_obj, message=str(ex))

        return return_obj

    @staticmethod
    def flatten_json(nested_json):
        """
            Flatten json object with nested keys into a single level.
            param:nested_json: A nested json object.
            :return: The flattened json object if successful, None otherwise.
        """

        result = flatten(nested_json)
        result['event_count'] = '1'

        return result
