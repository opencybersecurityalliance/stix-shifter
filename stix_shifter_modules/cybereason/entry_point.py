from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint


class EntryPoint(BaseEntryPoint):

    # python main.py translate synchronous_dummy query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate synchronous_dummy:dialect1 query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate synchronous_dummy:dialect2 query '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        if connection:
            self.setup_transmission_basic(connection, configuration)
        self.setup_translation_simple(dialect_default='default')
