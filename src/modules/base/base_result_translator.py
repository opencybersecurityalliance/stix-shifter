from abc import ABCMeta, abstractmethod


class BaseResultTranslator(object, metaclass=ABCMeta):

    def __init__(self, default_mapping_file_path=None):
        self.default_mapping_file_path = default_mapping_file_path

    @abstractmethod
    def translate_results(self, data, options, mapping=None):
        """
        Translates data into STIX results based on a mapping file
        :param data: data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given data to STIX. This should default to something if it hasn't been passed in
        :type mapping: str (filepath)
        :return: translated STIX formatted results
        :rtype: str
        """
        # if translating some datasource to STIX results...
        pass
