from abc import ABCMeta, abstractmethod


class BaseResultTranslator(object, metaclass=ABCMeta):

    def __init__(self, arg=None):
        self.arg = arg

    @abstractmethod
    def translate_results(self, data, mapping=None):
        # if translating some datasource to STIX results...
        pass
