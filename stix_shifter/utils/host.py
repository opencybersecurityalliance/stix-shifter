import requests
from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_transmission import stix_transmission
from flask import request
import json


class Host():

    def __init__(self):
        self.request_args = request.get_json(force=True)

        self.connection = self.request_args.get("connection")
        self.configuration = self.request_args.get("configuration")
        if self.connection:
            self.options = self.connection.get("options", {})
            # Overwrite proxy connection values with options
            self.connection['type'] = self.options.get('type')
            self.connection['port'] = self.options.get('port')
            self.connection['host'] = self.options.get('host')
        else:
            self.options = self.request_args.get("options", {})

    def transform_query(self):
        query = self.request_args["query"]
        print(self.request_args)
        translation_module = self.options.get('proxy', {}).get('type').lower()
        data_source_identity_object = '{}'

        if self.options['proxy'].get('proxy'):
            self.options['proxy'] = self.options['proxy'].pop('proxy')
            response = requests.post("http://{}:{}/transform_query".format(self.options['proxy'].get('host'), self.options['proxy'].get('port')),
                                     data=json.dumps({"query": query, "options": self.options}))
            return response.text
        else:
            self.options.pop('proxy', None)

        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'query', data_source_identity_object, query, self.options)
        return json.dumps(dsl['queries'])

    def translate_results(self, data_source_identity_object):
        data_source_results = self.request_args["results"]
        translation_module = self.options.get('proxy', {}).get('type').lower()

        if self.options['proxy'].get('proxy'):
            self.options['proxy'] = self.options['proxy'].pop('proxy')
            response = requests.post("http://{}:{}/translate_results".format(self.options['proxy'].get('host'), self.options['proxy'].get('port')),
                                     data=json.dumps({"results": data_source_results, "options": self.options}))
            return response.text
        else:
            self.options.pop('proxy', None)

        translation = stix_translation.StixTranslation()
        dsl = translation.translate(translation_module, 'results', data_source_identity_object, data_source_results, self.options)
        return json.dumps(dsl)

    def create_query_connection(self):
        query = self.request_args["query"]
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/create_query_connection".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration, "query": query}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return json.dumps(transmission.query(query))

    def create_status_connection(self):
        search_id = self.request_args["search_id"]
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/create_status_connection".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return json.dumps(transmission.status(search_id))

    def create_results_connection(self):
        search_id = self.request_args["search_id"]
        offset = self.request_args["offset"]
        length = self.request_args["length"]
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/create_results_connection".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id, "offset": offset, "length": length}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return json.dumps(transmission.results(search_id, offset, length))

    def delete_query_connection(self):
        search_id = self.request_args["search_id"]
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/delete_query_connection".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration, "search_id": search_id}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return json.dumps(transmission.delete(search_id))

    @staticmethod
    def ping(self):
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/ping".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return json.dumps(transmission.ping())

    def is_async(self):
        # Handle embedded proxies
        if self.options.get('options', {}).get('host'):
            self.connection['proxy_auth'] = self.options.get('proxy_auth')
            self.connection['options'] = self.options.get('options', {})
            response = requests.post("http://{}:{}/is_async".format(self.connection['host'], self.connection['port']),
                                     data=json.dumps({"connection": self.connection, "configuration": self.configuration}))
            return response.text

        transmission = stix_transmission.StixTransmission(self.connection['type'].lower(), self.connection, self.configuration)
        return "{}".format(transmission.is_async())
