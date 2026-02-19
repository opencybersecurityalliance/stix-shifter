import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from .api_client import APIClient
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
from stix_shifter_modules.crowdstrike_alerts.stix_transmission.api_client import APIResponseException
from requests.exceptions import ConnectionError


class Connector(BaseJsonSyncConnector):
    init_error = None
    logger = logger.set_logger(__name__)
    PROVIDER = 'CrowdStrike'
    IDS_LIMIT=500

    def __init__(self, connection, configuration):
        self.connector = __name__.split('.')[1]
        self.api_client = APIClient(connection, configuration)
        self.result_limit = connection['options'].get('result_limit', 10000)
        self.batchsize = connection['options'].get('batch_size')
        self.status = dict()
    
    async def ping_connection(self):
        return_obj = {}
        try:
            self.logger.debug(f"Attempting to ping the service for an auth token")
            response = await self.api_client.ping_box()
            response_code = response.code
            response_msg = response.read().decode('utf-8')
            if response_code == 200:
                self.logger.debug(f"Successfully pinged the device for an auth token")
                return_obj['success'] = True
            else:
                response_type = response.headers.get('Content-Type')
                raise APIResponseException(response_code, response_msg, response_type, response)
        except Exception as e:
            return self._handle_Exception(e)

        return return_obj

    async def create_results_connection(self, query, offset, length, metadata=None):
        #Initialize the starting offset and initial variables to empty.
        return_obj = dict()
        length = int(length)
        offset = int(offset)
        
        if(metadata == None):
            metadata = dict()
            current_offset = offset
            metadata["result_count"] = 0
        else:
            current_offset = metadata["offset"]
        
        try:
            #Query the alert endpoint to get a list of ID's. The ID's are in a list of list format.  
            alert_id_list = await self._get_alert_id(length, query, current_offset, metadata)
            
            #Separate the ID list into batchsize segments to be processed. 500 is the maximum.
            list_of_alert_id_list = [alert_id_list[x:x + min(500,self.batchsize)] for x in range(0, len(alert_id_list), min(500,self.batchsize))]
            
            #For each list of ID's, get the data from those ID's.
            alert_info = await self._get_alert_info(list_of_alert_id_list)
        except Exception as e:
            return self._handle_Exception(e)
                
        #If the total count is greater than the result limit, 
        if(metadata["offset"] > self.result_limit):
            alert_info = alert_info[0:(self.result_limit - offset)-1]
        
        if(metadata["result_count"] >= self.result_limit) or len(alert_info) < length:
            metadata = None
        
        return_obj["success"] = True
        return_obj["metadata"] = metadata
        return_obj["data"] = alert_info
        return return_obj
    
    async def _get_alert_id(self, length, query, current_offset, metadata):
        alert_id_list = []
        self.logger.debug(f"Collecting ID's using the following query/filter : {query}")
        while (len(alert_id_list) < length):
            #Get the next batch of ID's to process. We use length as batch size as this only gets the ID, not the data.
            #10000 is the maximum amount that can be asked for at once.
            self.logger.debug(f"Using the following settings to get a batch of ID's: offset : {current_offset}, length : {min(10000,length)}")

            get_ids_response = await self.api_client.get_alert_IDs(query, str(current_offset), str(min(10000,length)))
            if get_ids_response.code == 200:
                self.logger.debug(f"Successfully got a list of ID's")

                get_ids_data = get_ids_response.read().decode('utf-8')
                get_ids_json = json.loads(get_ids_data)
                if (len(get_ids_json.get('resources')) >= min(10000,length)):
                    alert_id_list.extend(get_ids_json.get('resources'))
                else:
                    alert_id_list.extend(get_ids_json.get('resources'))
                    current_offset = current_offset + len(get_ids_json.get('resources'))
                    break
                
                self.logger.debug(f"Did not reach the length requested, making another request")
                current_offset = current_offset + min(10000,length)
            else:
                raise APIResponseException(get_ids_response.code, get_ids_response.content, get_ids_response.headers.get('Content-Type'), get_ids_response)
        
        #We now know the next meta_data offset
        metadata["offset"] = current_offset
        return alert_id_list
    
    async def _get_alert_info(self, list_of_alert_id_list):
        alert_info = []
        for alert_id_list in list_of_alert_id_list:
            self.logger.debug(f"Requesting the following IDs : {alert_id_list}")

            alert_info_response = await self.api_client.get_alert_info(alert_id_list)
            if alert_info_response.code == 200:
                get_alert_info_data = alert_info_response.read().decode('utf-8')
                get_ids_json = json.loads(get_alert_info_data)
                alert_info.extend(get_ids_json['resources'])
            else:
                raise APIResponseException(alert_info_response.code, alert_info_response.content, alert_info_response.headers.get('Content-Type'), alert_info_response)
        return alert_info  
    
    def _handle_Exception(self, exception):
        response_dict = {}
        return_obj = {}
        try:
            raise exception
        except APIResponseException as ex:
            return self._handle_api_response(ex)
        except Exception as ex:
            ErrorResponder.fill_error(return_obj, response_dict, error=ex, connector=self.connector)
            return return_obj
        
        
    def _handle_api_response(self, rest_api_exception):
        response_dict = {}
        return_obj = {}
        connection_error = None
        
        if (rest_api_exception.content_header_type == 'application/json'):
            response = json.loads(rest_api_exception.error_message)
            response_dict['message'] = response['errors'][0]['message']
            if (rest_api_exception.error_code == 400):
                response_dict['type'] = 'ValidationError'
            elif (rest_api_exception.error_code == 401):
                response_dict['type'] = 'AuthenticationError'                    
        elif (rest_api_exception.content_header_type == 'text/html'):
            response = rest_api_exception.error_message
            connection_error = ConnectionError(f'Error connecting the datasource: {rest_api_exception.error_message}')
        else:
            raise Exception(rest_api_exception.error_message)
        
        ErrorResponder.fill_error(return_obj, response_dict, ['message'], error=connection_error, connector=self.connector)
        return return_obj