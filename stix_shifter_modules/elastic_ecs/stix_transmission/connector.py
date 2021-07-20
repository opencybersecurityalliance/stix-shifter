from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .api_client import APIClient
import json
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger


class UnexpectedResponseException(Exception):
    pass


class Connector(BaseSyncConnector):
    def __init__(self, connection, configuration):
        self.api_client = APIClient(connection, configuration)
        self.logger = logger.set_logger(__name__)
        self.host = Connector.get_host(connection)
        self.port = Connector.get_port(connection)

    @staticmethod
    def get_host(connection):
        return connection.get('host', None)

    @staticmethod
    def get_port(connection):
        return connection.get('port', None)

    def get_ds_link(self, _index, _id):
        if not self.host or not self.port:
            return None
        return 'https://%s:%d/%s/_all/%s' % (self.host, self.port, _index, _id)

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

    def ping_connection(self):
        response_txt = None
        return_obj = dict()
        try:
            response = self.api_client.ping_box()
            return self._handle_errors(response, return_obj)
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e

    def create_results_connection(self, query, offset, length):
        response_txt = None
        return_obj = dict()

        try:
            response = self.api_client.run_search(query, offset, length)
            return_obj = self._handle_errors(response, return_obj)

            if (return_obj['success']):
                response_json = json.loads(return_obj["data"])
                if response_json['hits']:
                    # and (response_json['hits']['total']['value'] >= 0 or response_json['hits']['total'] >= 0):
                    self.logger.error("Total # of hits:" + str(response_json['hits']['total']))
                    return_obj['data'] = [[record['_source'], record['_index'], record['_id']] for record in
                                          response_json["hits"]["hits"]]
                    self.logger.error("Total # of records: " + str(len(return_obj['data'])))
                    for event in return_obj['data']:
                        ds_link = self.get_ds_link(event[1], event[2])
                        event[0]['ds_link'] = ds_link

                    return_obj['data'] = [record[0] for record in return_obj['data']]



            return return_obj
        except Exception as e:
            if response_txt is not None:
                ErrorResponder.fill_error(return_obj, message='unexpected exception')
                self.logger.error('can not parse response: ' + str(response_txt))
            else:
                raise e
