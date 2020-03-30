from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.aws_security_hub_connector import Connector
from .stix_translation.query_translator import QueryTranslator

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        super().__init__(options)
        #TODO add transmission tests
        #TODO add translation tests
        if connection and configuration:
            connector = Connector(connection, configuration)
            self.setup_transmission_basic(connector)
        else:
            self.setup_translation_simple('default', query_translator=QueryTranslator())