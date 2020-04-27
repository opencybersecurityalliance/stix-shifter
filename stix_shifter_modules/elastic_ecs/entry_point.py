from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.results_translator import ResultTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)
        else:
            dialect = 'default'
            self.setup_translation_simple(dialect, results_translator=ResultTranslator(options, dialect))