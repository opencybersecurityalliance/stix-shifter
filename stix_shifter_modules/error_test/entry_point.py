from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.two_queries_query_translator import TwoQueriesQueryTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            self.setup_transmission_basic(connection, configuration)


        self.setup_translation_simple(dialect_default='default')
        two_queries_dialect = '2queries'
        two_queries_query_translator = TwoQueriesQueryTranslator(options, two_queries_dialect)
        self.add_dialect(two_queries_dialect, query_translator=two_queries_query_translator)
