from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator
import os

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        #TODO add transmission tests
        #TODO add translation tests
        if connection and configuration:
            self.setup_transmission_basic(connection, configuration)
        else:
            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath, "stix_translation"))

            dialect = 'default'
            self.setup_translation_simple(dialect_default=dialect, query_translator=QueryTranslator(options, dialect, filepath))
