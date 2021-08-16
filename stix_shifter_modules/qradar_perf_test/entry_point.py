from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
# from stix_shifter_modules.qradar_perf_test.stix_translation.results_translator import ResultsTranslator


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_basic(connection, configuration)

        self.setup_translation_simple(dialect_default='events')
