from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.cim_query_translator import CimQueryTranslator
from .stix_translation.car_query_translator import CarQueryTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_simple(connection, configuration)
        else:
            dialect = 'cim'
            self.add_dialect(dialect, query_translator=CimQueryTranslator(options, dialect), default=True)
            dialect = 'car'
            self.add_dialect(dialect, query_translator=CarQueryTranslator(options, dialect), default=False, default_include=False)