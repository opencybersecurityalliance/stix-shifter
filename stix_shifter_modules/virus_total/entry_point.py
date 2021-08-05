from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
import os
from .stix_translation.results_translator import ResultsTranslator


class EntryPoint(BaseEntryPoint):

    # python main.py translate virus_total results '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            self.setup_transmission_basic(connection, configuration)

        # Use default translation setup with default dialect otherwise...
        # self.setup_translation_simple(dialect_default='default')

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "stix_translation"))

        dialect = 'default'
        query_translator = QueryTranslator(options, dialect, filepath)
        results_translator = ResultsTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, results_translator=results_translator, default=True)