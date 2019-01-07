import importlib


TRANSMISSION_MODULES = ['async_dummy', 'synchronous_dummy', 'qradar', 'splunk', 'bigfix', 'csa', 'aws_security_hub']
RESULTS = 'results'
QUERY = 'query'
DELETE = 'delete'
STATUS = 'status'
PING = 'ping'
IS_ASYNC = 'is_async'


class StixTransmission:
    def __init__(self, module, connection, configuration):

        self.connector_module = importlib.import_module("stix_shifter.stix_transmission.src.modules." + module +
                                                        "." + module + "_connector")
        self.interface = self.connector_module.Connector(connection, configuration)

    def query(self, query):
        # Creates and sends a query to the correct datasource
        return self.interface.create_query_connection(query)

    def status(self, search_id):
        # Creates and sends a status query to the correct datasource asking for the status of the specific query
        return self.interface.create_status_connection(search_id)

    def results(self, search_id, offset, length):
        # Creates and sends a query to the correct datasource asking for results of the specific query
        return self.interface.create_results_connection(search_id, offset, length)

    def delete(self, search_id):
        # Sends a request to the correct datasource, asking to terminate a specific query
        return self.interface.delete_query_connection(search_id)

    def ping(self):
        # Creates and sends a ping request to confirm we are connected and authenticated
        return self.interface.ping()

    def is_async(self):
        # Check if the module is async/sync
        return self.interface.is_async
