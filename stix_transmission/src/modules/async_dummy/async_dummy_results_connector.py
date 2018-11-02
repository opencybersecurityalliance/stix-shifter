from ..base.base_results_connector import BaseResultsConnector
from ..base.base_status_connector import Status
import time

QUERY_ID_TABLE = {
    "uuid_1234567890": Status.COMPLETED.value,
    "uuid_not_done": Status.RUNNING.value,
    "uuid_should_error": Status.ERROR.value
}

RETURN_DUMMY_DATA = {
    "uuid_1234567890": "some data"
}


class AsyncDummyResultsConnector(BaseResultsConnector):
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def create_results_connection(self, query_id, offset, length):
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
        time.sleep(3)
        return_obj = {}

        if QUERY_ID_TABLE[query_id] == Status.COMPLETED.value and RETURN_DUMMY_DATA[query_id]:
            return_obj["success"] = True
            return_obj["data"] = RETURN_DUMMY_DATA[query_id]
        elif QUERY_ID_TABLE[query_id] == Status.RUNNING.value:
            return_obj["success"] = False
            return_obj["error"] = "Query is not finished processing"
        else:
            return_obj["success"] = False
            return_obj["error"] = "Error: query results not found"

        return return_obj
