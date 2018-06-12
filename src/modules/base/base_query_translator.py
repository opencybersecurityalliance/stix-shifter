from abc import ABCMeta, abstractmethod


class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, default_mapping_file_path=None):
        self.default_mapping_file_path = default_mapping_file_path

    @abstractmethod
    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into a different query format. Based on a mapping file
        :param data: STIX query string to transform into another format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """
        # if translating STIX pattern to a datasource query...
        pass
