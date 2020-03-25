from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.elastic_ecs_connector import Connector
from .stix_translation.results_translator import ResultTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)

        if connection:
            connector = Connector(connection, configuration)
            self.setup_transmission_basic(connector)
        else:
            self.setup_translation_simple('default', results_translator=ResultTranslator())