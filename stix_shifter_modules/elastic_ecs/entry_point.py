import os

from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "stix_translation"))

        dialect = 'default'
        query_translator = QueryTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, default_include=True, default=True)

        dialect = 'beats'
        query_translator = QueryTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, default_include=False, default=False)
