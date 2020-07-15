from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
import json
import requests
import copy


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.configuration = configuration
        self.request_http_path = "http://{}:{}".format(connection['host'], connection['port'])
        # deep copy connection since it will be mutates as it is passed along the proxy chain
        self.connection = self._unwrap_connection_options(copy.deepcopy(connection))

    def ping_connection(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(self.request_http_path + "/ping", data)
        return response.json()

    def create_query_connection(self, query):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query})
        response = requests.post(self.request_http_path + "/create_query_connection", data)
        return response.json()

    def create_results_connection(self, search_id, offset, length):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length})
        response = requests.post(self.request_http_path + "/create_results_connection", data)
        return response.json()

    def create_status_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(self.request_http_path + "/create_status_connection", data)
        return response.json()

    def delete_query_connection(self, search_id):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(self.request_http_path + "/delete_query_connection", data)
        return response.json()

    def is_async(self):
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(self.request_http_path + "/is_async", data)
        return response.text

    def _unwrap_connection_options(self, connection):
        connection_options = connection.get('options', {})
        embedded_connection_options = connection_options.get('options', {})
        if embedded_connection_options and embedded_connection_options.get('host'):
            connection['host'] = embedded_connection_options.get('host')
            connection['port'] = embedded_connection_options.get('port')
            connection['type'] = embedded_connection_options.get('type')
            del connection['options']
            connection.update(connection_options)
        elif connection_options and connection_options.get('host'):
            del connection['options']
            connection.update(connection_options)
        return connection
