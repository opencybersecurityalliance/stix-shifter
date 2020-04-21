from .base_data_mapper import BaseDataMapper

class EmptyDataMapper(BaseDataMapper):

    def __init__(self, options, dialect, basepath):
        self.options = options
        self.dialect = dialect
        self.basepath = basepath #used in tests
        self.map_data = {}

    def map_field(self, stix_object_name, stix_property_name):
        raise NotImplementedError()