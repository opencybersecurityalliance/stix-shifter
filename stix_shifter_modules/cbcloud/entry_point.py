from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)

        if connection:
            # Use default transmission setup otherwise...
            self.setup_transmission_simple(connection, configuration)

        self.setup_translation_simple(dialect_default='default')
