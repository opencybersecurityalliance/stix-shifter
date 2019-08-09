from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission
from flask import request
import json


class ProxyHost():

    def __init__(self):
        self.request_args = request.get_json(force=True)
        self.connection = self.request_args.get("connection")
        self.configuration = self.request_args.get("configuration")
        if self.connection:
            self.options = self.connection.get("options", {})
        else:
            self.connection = self.request_args.get("options", {})

    def transform_query(self):
        query = self.request_args["query"]
        data_source_identity_object = '{}'
        connection_options = self.connection.get('options', {})
        options = connection_options
        if connection_options:
            proxy_auth = connection_options.get('proxy_auth')
            embedded_connection_options = connection_options.get('options', {})
            if proxy_auth and embedded_connection_options and embedded_connection_options.get('host'):
                options = self.connection
        translation_module = self.connection['type'].lower()
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'query', data_source_identity_object, query, options)
        return json.dumps(dsl['queries'])

    def translate_results(self, data_source_identity_object):
        data_source_results = self.request_args["results"]
        connection_options = self.connection.get('options', {})
        options = connection_options
        if connection_options:
            proxy_auth = connection_options.get('proxy_auth')
            embedded_connection_options = connection_options.get('options', {})
            if proxy_auth and embedded_connection_options and embedded_connection_options.get('host'):
                options = self.connection
        translation_module = self.connection['type'].lower()
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'results', data_source_identity_object, data_source_results, options)
        return json.dumps(dsl)

    def create_query_connection(self):
        query = self.request_args["query"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.query(query))

    def create_status_connection(self):
        search_id = self.request_args["search_id"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.status(search_id))

    def create_results_connection(self):
        search_id = self.request_args["search_id"]
        offset = self.request_args["offset"]
        length = self.request_args["length"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.results(search_id, offset, length))

    def delete_query_connection(self):
        search_id = self.request_args["search_id"]
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.delete(search_id))

    def ping(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.ping())

    def is_async(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return "{}".format(transmission.is_async())
