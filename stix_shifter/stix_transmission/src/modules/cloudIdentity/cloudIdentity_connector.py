from ..base.base_connector import BaseConnector
from .apiclient import APIClient
from ..base.base_status_connector import Status
import json

from enum import Enum
from . import CloudIdentity_Request
#from CloudIdentity_Token import init



class DatasourceStatus(Enum):
    # WAIT, EXECUTE, SORTING, COMPLETED, CANCELED, ERROR
    WAIT = 'WAIT'
    EXECUTE = 'EXECUTE'
    SORTING = 'SORTING'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'

class Connector(BaseConnector):
    def __init__(self, connection, configuration):
        self.apiclient = APIClient(connection, configuration)
        self.ping_connector = self
        self.results_connector = self
        self.status_connector = self
        self.query_connector = self
        self.is_async = False
    def ping(self):
        try:
            response = self.api_client.ping_data_source()
            return response
        except Exception as err:
            print('error when pinging datasource {}:'.format(err))
            raise

    def _handle_errors(self, response, return_obj):
        response_code = response.code
        response_txt = response.read().decode('utf-8')

        if 200 <= response_code < 300:
            return_obj['success'] = True
            return_obj['data'] = response_txt
        elif ErrorResponder.is_plain_string(response_txt):
            ErrorResponder.fill_error(return_obj, message=response_txt)
        elif ErrorResponder.is_json_string(response_txt):
            response_json = json.loads(response_txt)
            ErrorResponder.fill_error(return_obj, response_json, ['reason'])
        else:
            raise UnexpectedResponseException
        return return_obj


    def create_query_connection(self, query):
       return {"success": True, "search_id": query}
        

    # Map data source status to connector status
    def __getStatus(self, status):
        switcher = {
            DatasourceStatus.WAIT.value: Status.RUNNING,
            DatasourceStatus.EXECUTE.value: Status.RUNNING,
            DatasourceStatus.SORTING.value: Status.RUNNING,
            DatasourceStatus.COMPLETED.value: Status.COMPLETED,
            DatasourceStatus.CANCELED.value: Status.CANCELED,
            DatasourceStatus.ERROR.value: Status.ERROR
        }
        return switcher.get(status).value

    def create_status_connection(self, search_id):
        try:
            response = self.apiclient.get_search_status(search_id)
            # Based on the response
            # return_obj['success'] = True or False
            # return_obj['status'] = One of the statuses as defined in the Status class:
            # Status.RUNNING, Status.COMPLETED, Status.CANCELED, Status.ERROR
            # return_obj['progress'] = Some progress code if returned from the API
            # Construct a response object
            response_code = response["code"]
            return_obj = dict()

            if response_code == 200:
                return_obj['success'] = True
                return_obj['status'] = self.__getStatus(response["status"])
            else:
                return_obj['success'] = False
                return_obj['error'] = response['message']
            return return_obj
        except Exception as err:
            print('error when getting search status: {}'.format(err))
            raise

    def create_results_connection(self, search_id, offset, length):
        response_txt = None
        return_obj = dict()
        try:
            # Grab the response, extract the response code, and convert it to readable json
            return_obj = self.apiclient.run_search(search_id)
            response_code = return_obj["success"]
            
            # Construct a response object
            if (response_code):
                #refine json response 
                if(return_obj['response']['report']['hits'] is not None):
                    response_json = return_obj['response']['report']['hits']

                #print(response_json)
             #   if response_json['hits']:
                    # and (response_json['hits']['total']['value'] >= 0 or response_json['hits']['total'] >= 0):
             #       print("Total # of hits:" + str(response_json['hits']['total']))
             #       return_obj['data'] = [record['_source'] for record in response_json["hits"]["hits"]]
             #       print("Total # of records: " + str(len(return_obj['data'])))

            #return return_obj
        except Exception as err:
            print('error when getting search results: {}'.format(err))
            raise

    def delete_query_connection(self, search_id):
        try:
            response = self.api_client.delete_search(search_id)
            return response
        except Exception as err:
            print('error when deleting search {}:'.format(err))
            raise
