from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils import logger
from flask import request
import json


class ProxyHost():

    def __init__(self):
        self.logger = logger.set_logger(__name__)
        self.request_args = request.get_json(force=True)
        self.connection = self.request_args.get("connection")
        self.configuration = self.request_args.get("configuration")
        if self.connection:
            self.options = self.connection.get("options", {})
        else:
            self.connection = self.request_args.get("options", {})

    def transform_query(self):
        query = self.request_args["query"]
        translation_module = self.connection['type'].lower()
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'query', '{}', query, self.connection)
        return json.dumps(dsl['queries'])

    def translate_results(self, data_source_identity_object):
        data_source_results = json.dumps(self.request_args["results"] )

        self.logger.debug(data_source_results)
        translation_module = self.connection['type'].lower()
        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'results', data_source_identity_object, data_source_results, self.connection)
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

    def ping_connection(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return json.dumps(transmission.ping())

    def is_async(self):
        transmission_module = self.connection['type'].lower()
        transmission = stix_transmission.StixTransmission(transmission_module, self.connection, self.configuration)
        return "{}".format(transmission.is_async())
