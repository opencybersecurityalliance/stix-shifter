import importlib
import traceback
from stix_shifter_utils.utils.module_discovery import dialect_list

class EntryPointBase:

    def parent_init(self, options):
        stack = traceback.extract_stack()
        self.__connector_module = stack[-2].filename.split('/')[-2]
        print("self.__connector_module: " + self.__connector_module)
        self.__dialect_to_translator = {}
        self.__dialect_to_data_mapper = {}
        self.__dialects_visible = []
        self.__options = options

    def add_dialect(self, dialect, translator, datamapper, default=False, default_include=True):
        self.__dialect_to_translator[dialect] = translator
        self.__dialect_to_data_mapper[dialect] = datamapper
        if default:
            self.__dialect_default = dialect
        if default_include:
            self.__dialects_visible.append(dialect)
        return self

    def init_standart(self, dialect_default):
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
