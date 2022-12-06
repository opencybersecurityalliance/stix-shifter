import os
import importlib
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_connector import BaseConnector
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)

        self.setup_translation_simple(dialect_default='SecurityAlert')

