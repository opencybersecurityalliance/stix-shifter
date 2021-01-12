from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.aql_query_translator import AqlQueryTranslator


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_simple(connection, configuration)
        else:
            self.setup_translation_simple(dialect_default='flows')
            dialect = 'aql'
            self.add_dialect(dialect,  AqlQueryTranslator(options, dialect, None), default_include=False, default=True)
