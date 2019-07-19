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
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/ping",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration}))
        return response.text

    def create_query_connection(self, query):
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/create_query_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query}))
        return response.text

    def create_results_connection(self, search_id, offset, length):
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/create_results_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length}))
        return response.text

    def create_status_connection(self, search_id):
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/create_status_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
        return response.text

    def delete_query_connection(self, search_id):
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/delete_query_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
        return response.text

    def _is_async(self):
        response = requests.post("http://" + self.proxy_host + ":" + self.proxy_port + "/is_async",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration}))
        return response.text

    def proxy_host(self, options):
        proxy_host = options.get('proxy', {}).get('host')
        if not proxy_host:
            raise Exception("Missing proxy host")
        return proxy_host

    def _proxy_port(self, options):
        proxy_port = options.get('proxy', {}).get('port')
        if not proxy_port:
            raise Exception("Missing proxy port")
        return proxy_port

    def _request_http_path(self, options):
        proxy_host = self._proxy_host(options)
        proxy_port = self._proxy_port(options)
        return "http://{}:{}".format(proxy_host, proxy_port)
