from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.delete_connector import DeleteConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.api_client import APIClient
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
import os


class EntryPoint(BaseEntryPoint):


    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        
        if connection:
            self.setup_transmission_simple(connection, configuration)
        
        self.setup_translation_simple(dialect_default='default')
