from ..base.base_connector import BaseConnector
import json
import requests


class Connector(BaseConnector):
    def __init__(self, connection, configuration):

        self.is_async = True

        self.connection = connection
        self.configuration = configuration

        self.results_connector = self
        self.status_connector = self
        self.delete_connector = self
        self.query_connector = self
        self.ping_connector = self

    def ping(self):
        response = requests.post("http://" + self.connection["proxy_host"] + ":" + self.connection["proxy_port"] + "/ping",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration}))
        return response.text

    def create_query_connection(self, query):
        response = requests.post("http://" + self.connection["proxy_host"] + ":" + self.connection["proxy_port"] + "/create_query_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query}))
        return response.text

    def create_results_connection(self, search_id, offset, length):
        response = requests.post("http://" + self.connection["proxy_host"] + ":" + self.connection["proxy_port"] + "/create_results_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length}))
        return response.text

    def create_status_connection(self, search_id):
        response = requests.get("http://" + self.connection["proxy_host"] + ":" + self.connection["proxy_port"] + "/create_status_connection",
                                data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
        return response.text

    def delete_query_connection(self, search_id):
        response = requests.post("http://" + self.connection["proxy_host"] + ":" + self.connection["proxy_port"] + "/delete_query_connection",
                                 data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
        return response.text
