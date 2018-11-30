from ..base.base_results_connector import BaseResultsConnector
import time

RETURN_DUMMY_DATA = {
    "obj_1": {},
    "obj_2": {},
    "obj_3": {},
    "obj_4": {},
    "obj_5": {},
}


class SynchronousDummyResultsConnector(BaseResultsConnector):
    def create_results_connection(self, params, options):
        """
        Creates a connection to the specified datasource to send a query

        :param params: the parameters for the query
        :param options: CLI options passed in

        :return: in dummy connectors, just returns passed in parameters
        """
        config = params['config']
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
        return_obj = {
            "response_code": 200,
            "query_results": RETURN_DUMMY_DATA
        }

        return return_obj
