from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.stix_bundle_translator import Translator
from .stix_transmission.stix_bundle_connector import Connector

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super(EntryPoint, self).__init__(options)
        self.set_async(False)
        if connection:
            connector = Connector(connection, configuration)
            self.setup_transmission_basic(connector)
        else:
            self.add_dialect('default', Translator(), None, True)