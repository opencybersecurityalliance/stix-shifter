from abc import ABCMeta, abstractmethod


class BaseResultTranslator(object, metaclass=ABCMeta):

    def __init__(self, arg=None):
        self.arg = arg

    @abstractmethod
    def translate_results(self, data, mapping=None):
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
