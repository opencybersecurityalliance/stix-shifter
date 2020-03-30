from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.data_mapper import DataMapper
from .stix_transmission.carbonblack_connector import Connector
from .stix_translation.query_translator import QueryTranslator
from .stix_translation.results_translator import ResultsTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)

        if connection:
            connector = Connector(connection, configuration)
            self.setup_transmission_basic(connector)
        else:
            self.add_dialect('default', query_translator=QueryTranslator(), results_translator=ResultsTranslator(), data_mapper=DataMapper(options), default=True)