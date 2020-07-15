from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.results_translator import ResultTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)
        else:
            dialect = 'default'
            self.setup_translation_simple(dialect_default=dialect, results_translator=ResultTranslator(options, dialect))