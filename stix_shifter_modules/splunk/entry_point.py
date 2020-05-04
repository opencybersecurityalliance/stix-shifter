from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.cim_query_translator import CimQueryTranslator
from .stix_translation.car_query_translator import CarQueryTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            self.setup_transmission_simple(connection, configuration)
        else:
            dialect = 'cim'
            self.add_dialect(dialect, query_translator=CimQueryTranslator(options, dialect), default=True)
            dialect = 'car'
            self.add_dialect(dialect, query_translator=CarQueryTranslator(options, dialect), default=False, default_include=False)