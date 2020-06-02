from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)

        if connection:
            self.setup_transmission_basic(connection, configuration)
        else:
            dialect = 'default'
            self.add_dialect(dialect, query_translator=QueryTranslator(options, dialect), results_translator=ResultsTranslator(options, dialect), default=True)