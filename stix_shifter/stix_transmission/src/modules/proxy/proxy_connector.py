from ..base.base_connector import BaseConnector
import json
import requests


class Connector(BaseConnector):
    def __init__(self, connection, configuration):

        self.connection = connection
        self.configuration = configuration
        self.proxy_host = self.connection['host']
        self.proxy_port = self.connection['port']

        connection_options = connection.get('options')

        self.connection['options'] = self.connection['options'].get('options', {})
        self.connection["proxy_auth"] = connection_options.get('proxy_auth')

        if not self.proxy_host:
            raise Exception("Missing proxy host")
        if not self.proxy_port:
            raise Exception("Missing proxy port")

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
        return response.text

    def create_query_connection(self, query):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query})
        response = requests.post(request_http_path + "/create_query_connection", data)
        return response.text

    def create_results_connection(self, search_id, offset, length):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length})
        response = requests.post(request_http_path + "/create_results_connection", data)
        return response.text

    def create_status_connection(self, search_id):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(request_http_path + "/create_status_connection", data)
        return response.text

    def delete_query_connection(self, search_id):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id})
        response = requests.post(request_http_path + "/delete_query_connection", data)
        return response.text

    def _is_async(self):
        request_http_path = "http://{}:{}".format(self.proxy_host, self.proxy_port)
        data = json.dumps({"connection": self.connection, "configuration": self.configuration})
        response = requests.post(request_http_path + "/is_async", data)
        return response.text
