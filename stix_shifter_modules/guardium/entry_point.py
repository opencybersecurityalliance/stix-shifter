from stix_shifter_utils.utils.entry_point_base import EntryPointBase

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)
        #TODO add test cases

        if connection:
            self.setup_transmission_simple(connection, configuration)
        else:
            self.setup_translation_simple('default')