from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.setup_translation_simple(dialect_default='at')