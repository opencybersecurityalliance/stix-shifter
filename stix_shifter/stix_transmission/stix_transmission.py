import importlib
from stix_shifter_utils.utils.error_response import ErrorResponder


RESULTS = 'results'
QUERY = 'query'
DELETE = 'delete'
STATUS = 'status'
PING = 'ping'
IS_ASYNC = 'is_async'


class StixTransmission:

    init_error = None

    def __init__(self, module, connection, configuration):
        module = module.split(':')[0]
        if connection.get('options', {}).get('proxy_host'):
            module = 'proxy'
        try:
            connector_module = importlib.import_module("stix_shifter_modules." + module + ".entry_point")
            self.entry_point = connector_module.EntryPoint(connection, configuration)
        except Exception as e:
            self.init_error = e

    def query(self, query):
        # Creates and sends a query to the correct datasource
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.create_query_connection(query)
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def status(self, search_id):
        # Creates and sends a status query to the correct datasource asking for the status of the specific query
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.create_status_connection(search_id)
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def results(self, search_id, offset, length):
        # Creates and sends a query to the correct datasource asking for results of the specific query
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.create_results_connection(search_id, offset, length)
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def delete(self, search_id):
        # Sends a request to the correct datasource, asking to terminate a specific query
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.delete_query_connection(search_id)
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def ping(self):
        # Creates and sends a ping request to confirm we are connected and authenticated
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.ping_connection()
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def is_async(self):
        # Check if the module is async/sync
        try:
            if self.init_error is not None:
                raise Exception(self.init_error)
            return self.entry_point.is_async()
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj
