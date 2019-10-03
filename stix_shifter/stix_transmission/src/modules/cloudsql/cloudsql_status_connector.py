from ..base.base_status_connector import BaseStatusConnector
from ..base.base_status_connector import Status
from enum import Enum
import json
import dateutil.parser


class CloudSQLStatus(Enum):
    # queued,running,completed,failed
    QUEUED = 'queued'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class CloudSQLStatusConnector(BaseStatusConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def __getStatus(self, cloudsql_status):
        switcher = {
            CloudSQLStatus.QUEUED.value: Status.RUNNING,
            CloudSQLStatus.RUNNING.value: Status.RUNNING,
            CloudSQLStatus.COMPLETED.value: Status.COMPLETED,
            CloudSQLStatus.FAILED.value: Status.ERROR,
        }
        return switcher.get(cloudsql_status).value

    def create_status_connection(self, search_id):
        success = False
        try:
            # Grab the response, already in json
            response = self.api_client.get_job(search_id)
            success = True
        except ValueError as e:
            response = {"message": repr(e)}
        except Exception as e:
            print('error when getting search results: {}'.format(e))
            raise

        response_json = response

        # Construct a response object
        return_obj = dict()
        return_obj['success'] = success
        if success:
            return_obj['status'] = self.__getStatus(response_json.get(
                                                    'status', 'failed'))
            if "end_time" in response_json and "submit_time" in response_json:
                # 2018-08-28T15:51:19.899Z
                # fmt = "%Y-%m-%dT%H:%M:%S.%f%Z"
                delta = dateutil.parser.parse(response_json.get('end_time')) -\
                    dateutil.parser.parse(response_json.get('submit_time'))
                return_obj['progress'] = delta.total_seconds()
            else:
                return_obj['progress'] = "0"
        else:
            return_obj['error'] = response_json['message']

        return return_obj
