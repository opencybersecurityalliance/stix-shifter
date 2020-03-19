from stix_shifter_utils.utils.entry_point_base import EntryPointBase

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        self.parent_init(options)
        self.init_standart('events')