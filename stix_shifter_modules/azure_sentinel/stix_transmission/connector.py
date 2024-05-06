import json
from azure.core.exceptions import ClientAuthenticationError
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class Connector(BaseJsonSyncConnector):
    api_client = None
    max_limit = 1000
    DEFAULT_API_VERSION = 'v1.0'
    LEGACY_ALERT = 'security/alerts'
    ALERT_V2 = 'security/alerts_v2'

    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]
        self.connection = connection
        self.configuration = configuration
        self.api_client = APIClient(self.connection, self.configuration)
        
        self.legacy_alert = connection['options'].get('alert')
        self.alert_v2 = connection['options'].get('alertV2')
        
        if self.legacy_alert:
            self.query_alert_type = 'alert'
            self.endpoint = '{api_version}/{api_resource}'.format(api_version=self.DEFAULT_API_VERSION, api_resource=self.LEGACY_ALERT)
        elif self.alert_v2:
            self.query_alert_type = 'alertV2'
            self.endpoint = '{api_version}/{api_resource}'.format(api_version=self.DEFAULT_API_VERSION, api_resource=self.ALERT_V2)
        else:
            raise Exception('Invalid alert resource type. At least one alert type must be selected.')

    async def ping_connection(self):
        """Ping the endpoint."""
        return_obj = dict()
        response_dict = dict()
        try:
            response = await self.api_client.ping_box(self.endpoint)
            response_code = response.code
            response_dict = json.loads(response.read())
            if 200 <= response_code < 300:
                return_obj['success'] = True
            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)
        except ClientAuthenticationError as ex:
            response_dict['code'] = 'unauthorized_client'
            response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)
        except Exception as ex:
            if "server timeout_error" in str(ex) or "timeout_error" in str(ex):
                response_dict['code'] = 'HTTPSConnectionError'
            else:
                response_dict['code'] = 'invalid_client'
            response_dict['error'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)

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
        response = None
        response_dict = dict()
        return_obj = dict()
        length = int(length)
        offset = int(offset)

        # total records is the sum of the offset and length(limit) value
        total_records = offset + length
        
        try:
            if not isinstance(query, dict):
                query = json.loads(query)

            query_service_type = list(query.keys())[0]
            query = query[query_service_type]
            
            if self.query_alert_type != query_service_type:
                self.logger.debug('Query type {} does not match the alert resource type {}'.format(query_service_type, self.query_alert_type))
                return_obj = {'success': True, "data": []}
                return return_obj
            
            # check for length value against the max limit(1000) of $top param in data source
            if length <= self.max_limit:
                # $skip(offset) param not included as data source provides incorrect results for some of the queries
                response = await self.api_client.run_search(query, total_records, self.endpoint)
            elif length > self.max_limit:
                response = await self.api_client.run_search(query, self.max_limit, self.endpoint)
            response_code = response.code
            response_dict = json.loads(response.read())
            if 199 < response_code < 300:
                return_obj['success'] = True
                return_obj['data'] = response_dict['value']
                while len(return_obj['data']) < total_records:
                    try:
                        next_page_link = response_dict['@odata.nextLink']
                        response = await self.api_client.next_page_run_search(next_page_link, self.endpoint)
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

                update_node = []

                # customize results for fileHashes
                for node in return_obj['data']:
                    if 'fileStates' in node:
                        for file in node["fileStates"]:
                            if file["fileHash"] is not None:
                                file["fileHash"][file["fileHash"]['hashType']] = file["fileHash"]['hashValue']
                                file["fileHash"].pop('hashType')
                                file["fileHash"].pop('hashValue')

                    if 'processes' in node:
                        for process in node["processes"]:
                            if process["fileHash"] is not None:
                                process["fileHash"][process["fileHash"]['hashType']] = process["fileHash"]['hashValue']
                                process["fileHash"].pop('hashType')
                                process["fileHash"].pop('hashValue')

                    if 'evidence' in node:
                        evidence_list = node['evidence']
                        
                        for evidence in evidence_list:
                            odata_type =  evidence.get('@odata.type').split('.')[3]
                            node[odata_type] = evidence
                        node.pop('evidence')  
                    
                    update_node.append(node)

                return_obj['data'] = update_node

            else:
                ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)

        except ClientAuthenticationError as ex:
            response_dict['code'] = 'unauthorized_client'
            response_dict['message'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)
        except Exception as ex:
            if "server timeout_error" in str(ex) or "timeout_error" in str(ex):
                response_dict['code'] = 'HTTPSConnectionError'
            else:
                response_dict['code'] = 'invalid_client'
            response_dict['error'] = str(ex)
            ErrorResponder.fill_error(return_obj, response_dict, ['error', 'message'], connector=self.connector)
        return return_obj

    
