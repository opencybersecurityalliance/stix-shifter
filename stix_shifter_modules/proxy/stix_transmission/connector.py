import copy
import json
from stix_shifter_utils.modules.base.stix_transmission.base_json_sync_connector import BaseJsonSyncConnector
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class Connector(BaseJsonSyncConnector):
    def __init__(self, connection, configuration):
        self.request_http_path = "https://{}:{}".format(connection['options']['proxy_host'], connection['options']['proxy_port'])
        self.timeout = connection['options']['timeout']
        self.connection, self.configuration = self._unwrap_connection_options(copy.deepcopy(connection), copy.deepcopy(configuration))
        self.client = RestApiClientAsync(connection['options']['proxy_host'], connection['options']['proxy_port'], url_modifier_function=lambda host_port, endpoint, headers: f'https://{host_port}{endpoint}', cert_verify=connection['options'].get('proxy_cert'))

    async def ping_connection(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = await self.client.call_api('/ping', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def create_query_connection(self, query):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query})
        response = await self.client.call_api('/create_query_connection', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source, metadata=None):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length, "data_source": data_source, "metadata": metadata})
        response = await self.client.call_api('/create_results_connection', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source, metadata=None):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length, "data_source": data_source, "metadata": metadata})
        response = await self.client.call_api('/create_results_stix_connection', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def create_status_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = await self.client.call_api('/create_status_connection', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def delete_query_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = await self.client.call_api('/delete_query_connection', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    async def is_async(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = await self.client.call_api('/is_async', 'POST', data=data, timeout=self.timeout)
        return json.loads(response.bytes)

    def _unwrap_connection_options(self, connection, configuration):
        if 'options' in connection and 'destination' in connection['options']:
            destination_params = connection['options']['destination']
            if type(destination_params) == str:
                if len(destination_params):
                    destination_params = json.loads(destination_params)
                else:
                    destination_params = {}
            if destination_params:
                return destination_params['connection'], destination_params['configuration']
        return connection, configuration
