from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)

        dialeat = 'event'
        self.add_dialect(dialeat, default=True)

        dialeat = 'process'
        self.add_dialect(dialeat,default=True)
