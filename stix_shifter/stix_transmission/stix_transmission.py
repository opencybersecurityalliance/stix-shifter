import asyncio
import functools
import importlib
from stix_shifter_utils.utils.error_response import ErrorResponder
import json


RESULTS = 'results'
RESULTS_STIX = 'results_stix'
QUERY = 'query'
DELETE = 'delete'
STATUS = 'status'
PING = 'ping'
IS_ASYNC = 'is_async'


class StixTransmission:

    init_error = None

    def respond_error(func):
        @functools.wraps(func)
        def wrapper_func(self, *args, **kwargs):
            try:
                if self.init_error:
                    raise self.init_error

                return func(self, *args, **kwargs)
            except Exception as ex:
                return_obj = dict()
                ErrorResponder.fill_error(return_obj, error=ex)
                return return_obj
        return wrapper_func

    def __init__(self, module, connection, configuration):
        module = module.split(':')[0]
        if connection.get('options', {}).get('proxy_host'):
            module = 'proxy'
        try:
            connector_module = importlib.import_module("stix_shifter_modules." + module + ".entry_point")
            self.entry_point = connector_module.EntryPoint(connection, configuration, connection.get('options', {}))
        except Exception as e:
            self.init_error = e

    @respond_error
    async def query_async(self, query):
        # Creates and sends a query to the correct datasource
        return await self.entry_point.create_query_connection(query)
    
    def query(self, query):
        return self.run_in_thread(self.query_async, query)

    @respond_error
    async def status_async(self, search_id):
        # Creates and sends a status query to the correct datasource asking for the status of the specific query
        return await self.entry_point.create_status_connection(search_id)
    
    def status(self, search_id):
        return self.run_in_thread(self.status_async, search_id)

    @respond_error
    async def results_async(self, search_id, offset, length):
        # Creates and sends a query to the correct datasource asking for results of the specific query
        return await self.entry_point.create_results_connection(search_id, offset, length)
  
    def results(self, search_id, offset, length):
        return self.run_in_thread(self.results_async, search_id, offset, length)

    @respond_error
    async def results_stix(self, search_id, offset, length, data_source):
        return await self.entry_point.create_results_stix_connection(search_id, offset, length, data_source)

    def results_stix(self, search_id, offset, length, data_source):
        return self.run_in_thread(self.results_stix, search_id, offset, length, data_source)

    @respond_error
    async def delete_async(self, search_id):
        # Sends a request to the correct datasource, asking to terminate a specific query
        return await self.entry_point.delete_query_connection(search_id)
        
    def delete(self, search_id):
        return self.run_in_thread(self.delete_async, search_id)

    @respond_error
    async def ping_async(self):
        # Creates and sends a ping request to confirm we are connected and authenticated
        return await self.entry_point.ping_connection()

    def ping(self):
        return self.run_in_thread(self.ping_async)

    def is_async(self):
        # Check if the module is async/sync
        try:
            if self.init_error:
                raise self.init_error
            return self.entry_point.is_async()
        except Exception as ex:
            return_obj = dict()
            ErrorResponder.fill_error(return_obj, error=ex)
            return return_obj

    def run_in_thread(self, callable, *args, **kwargs):
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(callable(*args, **kwargs))