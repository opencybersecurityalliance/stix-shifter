from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        #TODO add transmission tests
        #TODO add translation tests
        if connection and configuration:
            self.setup_transmission_basic(connection, configuration)
        else:
            self.setup_translation_simple(dialect_default='default', query_translator=QueryTranslator())