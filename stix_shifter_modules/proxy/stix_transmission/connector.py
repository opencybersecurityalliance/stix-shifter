from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
import json
import requests
import copy


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.request_http_path = "http://{}:{}".format(connection['options']['proxy_host'], connection['options']['proxy_port'])
        self.timeout = connection['options']['timeout']
        self.connection, self.configuration = self._unwrap_connection_options(copy.deepcopy(connection), copy.deepcopy(configuration))

    def ping_connection(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(self.request_http_path + "/ping", data, timeout=self.timeout)
        return response.json()

    def create_query_connection(self, query):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query})
        response = requests.post(self.request_http_path + "/create_query_connection", data, timeout=self.timeout)
        return response.json()

    def create_results_connection(self, search_id, offset, length):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length})
        response = requests.post(self.request_http_path + "/create_results_connection", data, timeout=self.timeout)
        return response.json()

    def create_status_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(self.request_http_path + "/create_status_connection", data, timeout=self.timeout)
        return response.json()

    def delete_query_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(self.request_http_path + "/delete_query_connection", data, timeout=self.timeout)
        return response.json()

    def is_async(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(self.request_http_path + "/is_async", data, timeout=self.timeout)
        return response.text

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
