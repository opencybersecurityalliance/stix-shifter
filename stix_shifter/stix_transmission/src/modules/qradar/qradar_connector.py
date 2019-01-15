from ..base.base_connector import BaseConnector
from ..base.base_status_connector import Status
from .arielapiclient import APIClient
from json import loads
from enum import Enum


class QRadarStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'


class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.is_async = True

        self.results_connector = self
        self.query_connector = self
        self.ping_connector = self
        self.delete_connector = self
        self.status_connector = self

    def ping(self):
        try:
            response = self.api_client.ping_box()
            response_code = response.code

            response_json = loads(response.read())

            return_obj = dict()
            return_obj['success'] = False

            if len(response_json) > 0 and response_code == 200:
                return_obj['success'] = True
            else:
                return_obj['error'] = response_json['message']

            return return_obj
        except Exception as err:
            print('error when pinging datasource {}:'.format(err))
            raise

    def create_query_connection(self, query):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.create_search(query)
            response_code = response.code
            response_json = loads(response.read())

            # Construct a response object
            return_obj = dict()

            if response_code == 201:
                return_obj['success'] = True
                return_obj['search_id'] = response_json['search_id']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when creating search: {}'.format(err))
            raise

    def __getStatus(self, qradar_status):
        switcher = {
            QRadarStatus.WAIT.value: Status.RUNNING,
            QRadarStatus.EXECUTE.value: Status.RUNNING,
            QRadarStatus.SORTING.value: Status.RUNNING,
            QRadarStatus.COMPLETED.value: Status.COMPLETED,
            QRadarStatus.CANCELED.value: Status.CANCELED,
            QRadarStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(qradar_status).value

    def create_status_connection(self, search_id):
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search(search_id)
            response_code = response.code
            response_json = loads(response.read())

            # Construct a response object
            return_obj = dict()

            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = self.__getStatus(response_json['status'])
                return_obj['progress'] = response_json['progress']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when getting search status: {}'.format(err))
            raise

    def create_results_connection(self, search_id, offset, length):
        min_range = offset
        max_range = offset + length
        # Grab the response, extract the response code, and convert it to readable json
        try:
            response = self.api_client.get_search_results(search_id, 'application/json', min_range, max_range)
            response_code = response.code

            # Construct a response object
            response_json = loads(response.read())
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
                return_obj['data'] = response_json['events']
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']
            return return_obj
        except Exception as err:
            print('error when getting search results: {}'.format(err))
            raise

    def delete_query_connection(self, search_id):
        try:
            response = self.api_client.delete_search(search_id)
            response_code = response.code
            response_json = loads(response.read())
            # Construct a response object
            return_obj = dict()
            if response_code == 202:
                return_obj['success'] = True
            else:
                return_obj['success'] = False
                return_obj['error'] = response_json['message']

            return return_obj
        except Exception as err:
            print('error when deleting search {}:'.format(err))
            raise
