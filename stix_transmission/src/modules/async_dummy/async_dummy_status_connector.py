from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status

QUERY_ID_TABLE = {
    "uuid_1234567890": Status.COMPLETED.value,
    "uuid_not_done": Status.RUNNING.value,
}


class AsyncDummyStatusConnector(BaseStatusConnector):
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def create_status_connection(self, query_id):
        # set headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # construct request object, purely for visual purposes in dummy implementation
        request = {
            "host": self.host,
            "path": self.path + query_id,
            "port": self.port,
            "headers": headers,
            "method": "GET"
        }

        print(request)
        return_obj = {}

        if query_id not in QUERY_ID_TABLE:
            return_obj["success"] = False
            return_obj["error"] = "query id does not exist"
        else:
            return_obj["success"] = True
            return_obj["status"] = QUERY_ID_TABLE[query_id]

        return return_obj
