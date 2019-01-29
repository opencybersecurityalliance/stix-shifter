from ..base.base_connector import BaseConnector
# from .synchronous_dummy_results_connector import SynchronousDummyResultsConnector
# from .synchronous_dummy_ping import SynchronousDummyPing
import time


class Connector(BaseConnector):
    def __init__(self):
        self.is_async = False

        self.results_connector = self
        self.ping_connector = self

    def ping(self):
        return "synchronous ping"

    def create_results_connection(self, params, options):
        """
        Creates a connection to the specified datasource to send a query

        :param params: the parameters for the query
        :param options: CLI options passed in

        :return: in dummy connectors, just returns passed in parameters
        """
        config = params['config']

        # The post-processed query, already translated from STIX SCO
        query = params['query']

        # set headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # construct request object, purely for visual purposes in dummy implementation
        request = {
            "host": config['host'],
            "path": config['path'] + query,
            "port": config['port'],
            "headers": headers,
            "method": "GET"
        }

        print(request)
        time.sleep(3)

        dummy_data = {"obj_1": {}, "obj_2": {}, "obj_3": {}, "obj_4": {}, "obj_5": {}}

        return_obj = {
            "response_code": 200,
            "query_results": dummy_data
        }

        return return_obj
