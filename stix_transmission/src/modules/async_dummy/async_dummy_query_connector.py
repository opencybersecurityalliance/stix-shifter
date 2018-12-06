from ..base.base_query_connector import BaseQueryConnector


class AsyncDummyQueryConnector(BaseQueryConnector):
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def create_query_connection(self, query):
        # set headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # construct request object, purely for visual purposes in dummy implementation
        request = {
            "host": self.host,
            "path": self.path + query,
            "port": self.port,
            "headers": headers,
            "method": "POST"
        }

        # return a mocked request
        print(request)

        return {
            "response_code": 200,
            "query_id": "uuid_1234567890"
        }
