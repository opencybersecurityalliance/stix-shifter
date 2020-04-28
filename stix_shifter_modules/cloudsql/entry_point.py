from stix_shifter_utils.utils.entry_point_base import EntryPointBase
import json

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            self.setup_transmission_simple(connection, configuration)