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
