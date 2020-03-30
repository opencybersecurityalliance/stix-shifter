from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.data_mapper import DataMapper
from .stix_transmission.synchronous_dummy_connector import Connector

from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix


class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)
        if connection:
            connector = Connector(connection, configuration)
            self.setup_transmission_basic(connector)
        else:
            self.add_dialect('default', data_mapper=DataMapper(options), default=True)