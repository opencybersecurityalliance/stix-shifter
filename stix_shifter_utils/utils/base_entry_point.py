import copy
import importlib
import traceback
import os
import functools
import json
import glob
from inspect import isawaitable
from typing import Union

from stix_shifter_utils.utils.module_discovery import dialect_list
from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
from stix_shifter_utils.modules.base.stix_transmission.base_delete_connector import BaseDeleteConnector
from stix_shifter_utils.modules.base.stix_transmission.base_query_connector import BaseQueryConnector
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import BaseStatusConnector
from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.modules.base.stix_transmission.base_json_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.param_validator import param_validator, modernize_objects, get_merged_config
from stix_shifter_utils.stix_translation.src.utils.exceptions import UnsupportedDialectException
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix

OPTION_LANGUAGE = 'language'


class BaseEntryPoint:

    def __init__(self, connection, configuration, options):
        self.__async = True
        stack = traceback.extract_stack()
        self.__connector_module = stack[-2].filename.split(os.sep)[-2]
        self.__dialect_to_query_translator = {}
        self.__dialect_to_results_translator = {}
        self.__dialects_all = []
        self.__dialects_active_default = []
        self.__dialect_default = {}
        self.__options = options

        self.__results_connector = None
        self.__status_connector = None
        self.__delete_connector = None
        self.__query_connector = None

        if connection:
            validation_obj = {'connection': connection, 'configuration': configuration}
            validation_obj = json.loads(json.dumps(validation_obj))
            modernize_objects(self.__connector_module, validation_obj)
            validation_obj = param_validator(self.__connector_module, validation_obj)
            connection.clear()
            configuration.clear()
            options.clear()
            connection.update(validation_obj['connection'])
            options.update(validation_obj['connection']['options'])
            configuration.update(validation_obj['configuration'])

    def translation(func):
        @functools.wraps(func)
        def wrapper_func(self, *args, **kwargs):
            self.__check_translation_configured()
            return func(self, *args, **kwargs)
        return wrapper_func

    def __check_translation_configured(self):
        if not self.__dialect_default:
            raise Exception('EntryPoint: default dialect is not configured')

    def transmission(func):
        @functools.wraps(func)
        def wrapper_func(self, *args, **kwargs):
            self.__check_transmission_configured()
            return func(self, *args, **kwargs)
        return wrapper_func

    def __check_transmission_configured(self):
        if not(self.__results_connector and self.__status_connector and self.__delete_connector and self.__query_connector):
            raise Exception('EntryPoint: one of transmission connectors is not configured')

    def add_dialect(self, dialect, query_translator=None, results_translator=None, default=False, default_include=True):
        if not query_translator:
            query_translator = self.create_default_query_translator(dialect)
        if not results_translator:
            results_translator = self.create_default_results_translator(dialect)
        if not (isinstance(query_translator, BaseQueryTranslator)):
            raise Exception('query_translator is not instance of BaseQueryTranslator')
        if not (isinstance(results_translator, BaseResultTranslator)):
            raise Exception('results_translator is not instance of BaseResultTranslator')
        self.__dialect_to_query_translator[dialect] = query_translator
        self.__dialect_to_results_translator[dialect] = results_translator
        if default:
            self.__dialect_default[query_translator.get_language()] = dialect
        self.__dialects_all.append(dialect)
        if default_include:
            self.__dialects_active_default.append(dialect)
        return self

    def setup_translation_simple(self, dialect_default, query_translator=None, results_translator=None):
        module_name = self.__connector_module
        dialects = dialect_list(module_name, self.__options) # get list of dialects from configuration
        for dialect in dialects:
            if self.__options:
                is_default = True
            else:
                is_default = (dialect == dialect_default)
            self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator,
                             default=is_default)

    def create_default_query_translator(self, dialect):
        module_name = self.__connector_module
        module = importlib.import_module(
                    "stix_shifter_modules." + module_name + ".stix_translation.query_translator")
        basepath = os.path.dirname(module.__file__)
        mapping_filepath = os.path.abspath(basepath)
        query_translator = module.QueryTranslator(self.__options, dialect, mapping_filepath)
        return query_translator

    def create_default_results_translator(self, dialect):
        module_name = self.__connector_module
        dir_path = "stix_shifter_modules." + module_name + ".stix_translation"
        file_path = dir_path + ".results_translator"
        try:
            module = importlib.import_module(file_path)
            basepath = os.path.dirname(module.__file__)
            mapping_filepath = os.path.abspath(basepath)
            results_translator = module.ResultsTranslator(self.__options, dialect, mapping_filepath)
        except:
            module = importlib.import_module(dir_path)
            basepath = os.path.dirname(module.__file__)
            mapping_filepath = os.path.abspath(basepath)
            results_translator = JSONToStix(self.__options, dialect, mapping_filepath)
        return results_translator

    @translation
    def get_mapping(self):
        module_name = self.__connector_module
        module = importlib.import_module(
                    "stix_shifter_modules." + module_name + ".stix_translation")
        basepath = os.path.dirname(module.__file__)
        basepath = os.path.abspath(basepath)
        basepath = os.path.join(basepath, 'json')

        mapping = {}
        if os.path.isdir(basepath):
            for filename in glob.glob(basepath + os.sep + "*.json"):
                key = os.path.basename(filename)[:-5]
                with open(filename, 'r') as f:
                    jsondata = json.load(f)
                    mapping[key] = jsondata
        return mapping

    @translation
    def get_query_translator(self, dialect=None):
        try:
            if dialect:
                return self.__dialect_to_query_translator[dialect]
            return self.__dialect_to_query_translator[self.__dialect_default[self.__options.get(OPTION_LANGUAGE, "stix")]]
        except KeyError as ex:
            raise UnsupportedDialectException(dialect)
        
    @translation
    def __combine_default_results_translator_to_stix_maps(self, dialects:list=None):
        """
        Returns default or dialect specific ResultTranslator. 
        If there are multiple dialects in the module and 'dialects' list argument is specified, the return combines
        the corresponding ResultTranslators' map_data into a copy of the default ResultTranslator and returns it.
        """
        default_results_translator:BaseResultTranslator = self.__dialect_to_results_translator[self.__dialect_default[self.__options.get(OPTION_LANGUAGE, "stix")]]
        results_translator = copy.deepcopy(default_results_translator)

        for dialect, translator in self.__dialect_to_results_translator.items():
            if dialects and dialect not in dialects:
                continue
            results_translator.map_data = {**results_translator.map_data, **translator.map_data}

        return results_translator


    @translation
    def get_results_translator(self, dialect:Union[str,list]=None):
        if dialect and isinstance(dialect, str):
            return self.__dialect_to_results_translator[dialect]
        return self.__combine_default_results_translator_to_stix_maps(dialect)

    @translation
    async def parse_query(self, data):
        translator = self.get_query_translator()
        result = translator.parse_query(data)
        if isawaitable(result):
            result = await result
        return result

    @translation
    async def transform_query(self, dialect, data):
        translator = self.get_query_translator(dialect)
        result = translator.transform_query(data)
        if isawaitable(result):
            result = await result
        return result

    @translation
    async def translate_results(self, data_source, data):
        dialects = None
        if 'dialects' in self.__options:
            dialects = self.__options['dialects']

        translator = self.get_results_translator(dialects)
        try:
            result = translator.translate_results(data_source, data)
            if isawaitable(result):
                result = await result
            return result
        except Exception as ex:
            result = {}
            ErrorResponder.fill_error(result, message_struct={'exception': ex})
            return result

    @translation
    def get_dialects(self, include_hidden=False):
        if include_hidden:
            return self.__dialects_all
        return self.__dialects_active_default
    
    @translation
    def get_configs_full(self):
        return get_merged_config(self.__connector_module)

    @translation
    def get_dialects_full(self):
        result = {}
        for dialect in self.__dialects_all:
            query_translator = self.get_query_translator(dialect)
            dialect_item = {}
            dialect_item['language'] = query_translator.get_language()
            dialect_item['default'] = dialect in self.__dialects_active_default
            result[dialect] = dialect_item
        return result

    def setup_transmission_simple(self, connection, configuration):
        module_name = self.__connector_module
        module_path = "stix_shifter_modules." + module_name + ".stix_transmission"
        module = importlib.import_module(module_path + ".api_client")
        api_client = module.APIClient(connection, configuration)

        module = importlib.import_module(module_path + ".ping_connector")
        connector = module.PingConnector(api_client)
        self.set_ping_connector(connector)

        module = importlib.import_module(module_path + ".query_connector")
        connector = module.QueryConnector(api_client)
        self.set_query_connector(connector)

        module = importlib.import_module(module_path + ".status_connector")
        connector = module.StatusConnector(api_client)
        self.set_status_connector(connector)

        module = importlib.import_module(module_path + ".results_connector")
        connector = module.ResultsConnector(api_client)
        self.set_results_connector(connector)

        module = importlib.import_module(module_path + ".delete_connector")
        connector = module.DeleteConnector(api_client)
        self.set_delete_connector(connector)

    def setup_transmission_basic(self, connection, configuration):
        module_name = self.__connector_module
        module_path = "stix_shifter_modules." + module_name + ".stix_transmission"
        module = importlib.import_module(module_path + ".connector")
        connector = module.Connector(connection, configuration)

        if not isinstance(connector, BaseConnector):
            raise Exception('connector is not instance of BaseConnector')
        self.set_query_connector(connector)
        self.set_status_connector(connector)
        self.set_results_connector(connector)
        self.set_delete_connector(connector)
        self.set_ping_connector(connector)

    def set_query_connector(self, connector):
        if not (isinstance(connector, (BaseConnector, BaseQueryConnector)) or issubclass(connector, BaseConnector)):
            raise Exception('connector is not instance of BaseConnector (or it\'s subclass) or BaseQueryConnector')
        self.__query_connector = connector

    @transmission
    async def create_query_connection(self, query):
        result = self.__query_connector.create_query_connection(query)
        if isawaitable(result):
            result = await result
        return result

    def set_status_connector(self, connector):
        if not (isinstance(connector, (BaseConnector, BaseStatusConnector)) or issubclass(connector, BaseConnector)):
            raise Exception('connector is not instance of BaseConnector (or it\'s subclass) or BaseStatusConnector')
        self.__status_connector = connector

    @transmission
    async def create_status_connection(self, search_id, metadata=None):
        result = None
        if metadata:
            result = self.__status_connector.create_status_connection(search_id, metadata)
        else:
            result = self.__status_connector.create_status_connection(search_id)
        if isawaitable(result):
            result = await result
        return result

    def set_results_connector(self, connector):
        if not isinstance(connector, (BaseConnector, BaseResultsConnector)):
            raise Exception('connector is not instance of BaseConnector or BaseResultsConnector')
        self.__results_connector = connector

    @transmission
    async def create_results_connection(self, search_id, offset, length, metadata=None):
        result = None
        if metadata:
            result = self.__results_connector.create_results_connection(search_id, offset, length, metadata)
        else:
            result = self.__results_connector.create_results_connection(search_id, offset, length)
        if isawaitable(result):
            result = await result
        return result


    @transmission
    async def create_results_stix_connection(self, search_id, offset, length, data_source, metadata=None):
        result = None
        if metadata:
            result = self.__results_connector.create_results_stix_connection(self, search_id, offset, length, data_source, metadata) 
        else:
            result = self.__results_connector.create_results_stix_connection(self, search_id, offset, length, data_source)
        if isawaitable(result):
            result = await result
        return result        

    def set_delete_connector(self, connector):
        if not isinstance(connector, (BaseConnector, BaseDeleteConnector)):
            raise Exception('connector is not instance of BaseConnector or BaseDeleteConnector')
        self.__delete_connector = connector

    @transmission
    async def delete_query_connection(self, search_id):
        result = self.__delete_connector.delete_query_connection(search_id)
        if isawaitable(result):
            result = await result
        return result   


    def set_ping_connector(self, connector):
        if not isinstance(connector, (BaseConnector, BasePingConnector)):
            raise Exception('connector is not instance of BaseConnector or BasePingConnector')
        self.__ping_connector = connector

    @transmission
    async def ping_connection(self):
        result = self.__ping_connector.ping_connection()
        if isawaitable(result):
            result = await result
        return result   

    def set_async(self, is_async):
        self.__async = is_async

    def is_async(self):
        return self.__async
