from stix_shifter_utils.utils.entry_point_base import EntryPointBase

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)
        else:
            self.add_dialect('default', default=True)