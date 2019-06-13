from abc import ABCMeta, abstractmethod


class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, default_mapping_file_path=None):
        self.default_mapping_file_path = default_mapping_file_path

    @abstractmethod
    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):
        """
        Transforms STIX pattern into a different query format. Based on a mapping file
        :param data: STIX pattern to transform into native data source query
        :type data: str
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :data_model_mapper: Mapping object for the data source
        :type data_model_mapper: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """
        # if translating STIX pattern to a datasource query...
        pass
