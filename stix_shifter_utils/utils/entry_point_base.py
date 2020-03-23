import importlib
import traceback
from stix_shifter_utils.utils.module_discovery import dialect_list
import os

import sys, inspect


class EntryPointBase:

    def __init__(self, options):
        self.__async = True
        stack = traceback.extract_stack()
        self.__connector_module = stack[-2].filename.split('/')[-2]
        self.__dialect_to_translator = {}
        self.__dialect_to_data_mapper = {}
        self.__dialects_visible = []
        self.__options = options

        self.__results_connector = None
        self.__status_connector = None
        self.__delete_connector = None
        self.__query_connector = None

    def add_dialect(self, dialect, translator, datamapper, default=False, default_include=True):
        self.__dialect_to_translator[dialect] = translator
        self.__dialect_to_data_mapper[dialect] = datamapper
        if default:
            self.__dialect_default = dialect
        if default_include:
            self.__dialects_visible.append(dialect)
        return self

    def setup_translation_simple(self, dialect_default):
        module = self.__connector_module
        dialects = dialect_list(module)
        
        translator_module = importlib.import_module(
                    "stix_shifter_modules." + module + ".stix_translation." + module + "_translator")
        datamapper_module = importlib.import_module(
                    "stix_shifter_modules." + module + ".stix_translation.data_mapping")
        for dialect in dialects:
            self.add_dialect(dialect, translator_module.Translator(dialect), datamapper_module.DataMapper(self.__options, dialect), default=(dialect==dialect_default))

    def get_data_mapper(self, dialect=None):
        if dialect:
            return self.__dialect_to_data_mapper[dialect]
        return self.__dialect_to_data_mapper[self.__dialect_default]


    def get_translator(self, dialect=None):
        if dialect:
            return self.__dialect_to_translator[dialect]
        return self.__dialect_to_translator[self.__dialect_default]

    def transform_query(self, dialect, data, antlr_parsing, data_model_mapper, options):
        translator = self.get_translator(dialect)
        return translator.transform_query(data, antlr_parsing, data_model_mapper, options)


    def translate_results(self, data_source, data, options):
        translator = self.get_translator()
        return translator.translate_results(data_source, data, options)

    def get_dialects(self):
        return self.__dialects_visible

    def setup_transmission_basic(self, connector):
        self.set_query_connector(connector)
        self.set_status_connector(connector)
        self.set_results_connector(connector)
        self.set_delete_connector(connector)
        self.set_ping_connector(connector)

    def set_query_connector(self, connector):
        self.__query_connector = connector

    def create_query_connection(self, query):
        return self.__query_connector.create_query_connection(query)

    def set_status_connector(self, connector):
        self.__status_connector = connector

    def create_status_connection(self, search_id):
        return self.__status_connector.create_status_connection(search_id)
    
    def set_results_connector(self, connector):
        self.__results_connector = connector

    def create_results_connection(self, search_id, offset, length):
        return self.__results_connector.create_results_connection(search_id, offset, length)

    def set_delete_connector(self, connector):
        self.__delete_connector = connector

    def delete_query_connection(self, search_id):
        return self.__delete_connector.delete_query_connection(search_id)

    def set_ping_connector(self, connector):
        self.__ping_connector = connector

    def ping_connection(self):
        #TODO rename ping to ping_connection?
        return self.__ping_connector.ping()

    def set_async(self, async):
        self.__async = async

    def is_async(self):
        return self.__async
