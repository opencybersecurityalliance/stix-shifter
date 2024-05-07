from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
from .stix_translation.query_translator import QueryTranslator


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_simple(connection, configuration)

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(base_path, "stix_translation"))

        dialect = 'default'
        query_translator = QueryTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, default_include=True, default=True)

        dialect = 'cloud_siem'
        query_translator = QueryTranslator(options, dialect, filepath)
        self.add_dialect(dialect, query_translator=query_translator, default_include=False, default=False)

