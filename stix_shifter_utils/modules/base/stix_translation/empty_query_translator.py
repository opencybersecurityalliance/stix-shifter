from .base_query_translator import BaseQueryTranslator

class EmptyQueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath=None):
        self.options = options
        self.dialect = dialect
        self.basepath = basepath #used in tests
        self.map_data = {}
        self.select_fields = {}

    def map_field(self, stix_object_name, stix_property_name):
        raise NotImplementedError()