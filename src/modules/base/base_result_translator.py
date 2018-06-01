from abc import ABCMeta, abstractmethod


class BaseResultTranslator(object, metaclass=ABCMeta):

    @abstractmethod
    def translate_results(self, data, mapping=None):
        # if translating some datasource to STIX results...
        pass
