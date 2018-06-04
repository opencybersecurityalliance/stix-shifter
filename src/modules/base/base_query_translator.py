from abc import ABCMeta, abstractmethod


class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, arg=None):
        self.arg = arg

    @abstractmethod
    def transform_query(self, data, mapping=None):
        # if translating STIX pattern to a datasource query...
        pass
