from abc import ABCMeta, abstractmethod
from .base_result_translator import BaseResultTranslator
from .base_query_translator import BaseQueryTranslator


class BaseTranslator:

    def __init__(self):
        self.result_translator = BaseResultTranslator()
        self.query_translator = BaseQueryTranslator()

    def translate_results(self, data_source, data, options, mapping=None):
        """
        Translates data into STIX results based on a mapping file
        :param data_source: STIX identity object representing a data source
        :type data_source: str
        :param data: data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given data to STIX.
        :type mapping: str (filepath)
        :return: translated STIX formatted results
        :rtype: str
        """
        return self.result_translator.translate_results(data_source, data, options, mapping)

    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):
        """
        Transforms STIX query into a different query format. based on a mapping file
        :param data: STIX pattern to transform into native data source query
        :type data: str
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :data_model_mapper: Mapping object for the data source
        :type data_model_mapper: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX pattern into native data source query.
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        return self.query_translator.transform_query(data, antlr_parsing_object, data_model_mapper, options, mapping)
