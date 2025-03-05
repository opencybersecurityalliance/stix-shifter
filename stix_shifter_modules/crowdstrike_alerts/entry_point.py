from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)

        if connection:
            self.setup_transmission_basic(connection, configuration)

        self.add_dialect('default', default=True)

    def handle_custom_mapping(self, custom_mapping):
        if custom_mapping and custom_mapping['to_stix_mapping']:
            self.add_dialect('default', custom_mapping=custom_mapping)
