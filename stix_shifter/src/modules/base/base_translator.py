from abc import ABCMeta, abstractmethod
from .base_result_translator import BaseResultTranslator
from .base_query_translator import BaseQueryTranslator
from stix2patterns.validator import run_validator


class StixValidationException(Exception):
    pass


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
        :param mapping: The mapping file path to use as instructions on how to translate the given data to STIX. This should default to something if it hasn't been passed in
        :type mapping: str (filepath)
        :return: translated STIX formatted results
        :rtype: str
        """
        return self.result_translator.translate_results(data_source, data, options, mapping)

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into a different query format. based on a mapping file
        :param data: STIX query string to transform into another format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        errors = run_validator(data)
        if (errors != []):
            raise StixValidationException(
                "The STIX pattern has the following errors: {}".format(errors))
        else:
            return self.query_translator.transform_query(data, options, mapping)
