from ..base.base_connector import BaseConnector
import json
import requests


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.configuration = configuration
        self.proxy_host = connection['host']
        self.proxy_port = connection['port']
        self.connection = self._unwrap_connection_options(connection)
        self.results_connector = self
        self.status_connector = self
        self.delete_connector = self
        self.query_connector = self
        self.ping_connector = self
        self.is_async = self._is_async()

    def ping(self):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(request_http_path + "/ping", data)
        return response.json()

    def create_query_connection(self, query):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query})
        response = requests.post(request_http_path + "/create_query_connection", data)
        return response.json()

    def create_results_connection(self, search_id, offset, length):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length})
        response = requests.post(request_http_path + "/create_results_connection", data)
        return response.json()

    def create_status_connection(self, search_id):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(request_http_path + "/create_status_connection", data)
        return response.json()

    def delete_query_connection(self, search_id):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(request_http_path + "/delete_query_connection", data)
        return response.json()

    def _is_async(self):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(request_http_path + "/is_async", data)
        return response.text

    def _unwrap_connection_options(self, connection):
        connection_options = connection.get('options', {})
        if connection_options:
            proxy_auth = connection_options.get('proxy_auth')
            embedded_connection_options = connection_options.get('options', {})
            if proxy_auth and embedded_connection_options and embedded_connection_options.get('host'):
                connection['proxy_auth'] = connection['options'].pop('proxy_auth')
                connection['host'] = connection['options']['options'].pop('host')
                connection['port'] = connection['options']['options'].pop('port')
                connection['type'] = connection['options']['options'].pop('type')
                # TODO: This may overwrite stuff in the outer-most options we want to keep
                connection['options'] = connection['options'].pop('options')
        return connection
