from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_transmission.api_client import APIClient
from .stix_transmission.ping_connector import PingConnector
from .stix_transmission.query_connector import QueryConnector
from .stix_transmission.status_connector import StatusConnector
from .stix_transmission.results_connector import ResultsConnector
from .stix_transmission.delete_connector import DeleteConnector
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator
import os


class EntryPoint(BaseEntryPoint):

    # python main.py translate async_dummy query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate async_dummy:dialect1 query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate async_dummy:dialect2 query '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_simple(connection, configuration)

        self.setup_translation_simple(dialect_default='default')

