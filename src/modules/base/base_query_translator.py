from abc import ABCMeta, abstractmethod


class BaseQueryTranslator(object, metaclass=ABCMeta):

    @abstractmethod
    def transform_query(self, data, mapping=None):
        # if translating STIX pattern to a datasource query...
        pass
