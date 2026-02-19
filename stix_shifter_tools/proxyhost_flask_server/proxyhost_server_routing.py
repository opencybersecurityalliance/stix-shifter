import json
from flask import Flask, request

from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils import logger
from flask import request
import json
    
# Start a local web service for STIX shifter, to use in combination with the proxy data source
# module. This combination allows one to run and debug their stix-shifter code locally, while interacting with
# it inside a service provider such as IBM Security Connect

def start_proxyhost_flask_server(data_source):
    app = Flask("stix-shifter")

    @app.route('/transform_query', methods=['POST'])
    def transform_query():
        host = ProxyHost()
        return host.transform_query()

    @app.route('/translate_results', methods=['POST'])
    def translate_results():
        data_source_identity_object = data_source
        host = ProxyHost()
        return host.translate_results(data_source_identity_object)

    @app.route('/create_query_connection', methods=['POST'])
    def create_query_connection():
        host = ProxyHost()
        return host.create_query_connection()

    @app.route('/create_status_connection', methods=['POST'])
    def create_status_connection():
        host = ProxyHost()
        return host.create_status_connection()

    @app.route('/create_results_connection', methods=['POST'])
    def create_results_connection():
        host = ProxyHost()
        return host.create_results_connection()

    @app.route('/delete_query_connection', methods=['POST'])
    def delete_query_connection():
        host = ProxyHost()
        return host.delete_query_connection()

    @app.route('/ping', methods=['POST'])
    def ping_connection():
        host = ProxyHost()
        return host.ping_connection()

    @app.route('/is_async', methods=['POST'])
    def is_async():
        host = ProxyHost()
        return host.is_async()
    
    return app
    
class ProxyHost():
    def __init__(self):
        self.logger = logger.set_logger(__name__)
        self.request_args = request.get_json(force=True)
        self.connection = self.request_args.get("connection")
        self.configuration = self.request_args.get("configuration")
        self.module = self.request_args.get("module")
        if self.connection:
            self.options = self.connection.get("options", {})
        else:
            self.options = self.request_args.get("options", {})

    def transform_query(self):
        query = self.request_args["data"]
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(self.module, 'query', '{}', query, self.options)
        return json.dumps(dsl)

    def translate_results(self, data_source_identity_object):
        data_source_results = self.request_args["data"]
        data_source = self.request_args.get("data_source")
        if data_source_identity_object:
            data_source = data_source_identity_object

        self.logger.debug(data_source_results)
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(self.module, 'results', data_source, data_source_results, self.options)
        return json.dumps(dsl)

    async def create_query_connection(self):
        query = self.request_args["query"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.query(query))

    async def create_status_connection(self):
        search_id = self.request_args["search_id"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.status(search_id))

    async def create_results_connection(self):
        search_id = self.request_args["search_id"]
        offset = self.request_args["offset"]
        length = self.request_args["length"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.results(search_id, offset, length))

    async def delete_query_connection(self):
        search_id = self.request_args["search_id"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.delete(search_id))

    async def ping_connection(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.ping())

    def is_async(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return "{}".format(transmission.is_async())