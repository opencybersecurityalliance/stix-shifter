from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator
import os

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)

        if connection:
            self.setup_transmission_basic(connection, configuration)
        else:

            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath, "stix_translation"))

            dialect = 'default'
            self.add_dialect(dialect, query_translator=QueryTranslator(options, dialect, basepath), results_translator=ResultsTranslator(options, dialect, basepath), default=True)
