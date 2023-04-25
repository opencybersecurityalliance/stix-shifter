from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(False)
        print(options)
        dialects = []
        if options['alert']:
            dialects.append('alert')
        elif options['alertV2']:
            dialects.append('alertV2')
        else:
            raise Exception('At least one alert type must be selected!')
        
        options['dialects'] = dialects
        print(options)
        if connection:
            self.setup_transmission_basic(connection, configuration)

        self.setup_translation_simple(dialect_default='alert')