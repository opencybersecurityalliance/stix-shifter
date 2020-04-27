from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from stix_shifter_utils.modules.cim.stix_translation.cim_data_mapper import CimDataMapper
from stix_shifter_utils.modules.car.stix_translation.car_data_mapper import CarDataMapper

class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        if connection:
            self.setup_transmission_simple(connection, configuration)
        else:
            dialect = 'cim'
            self.add_dialect(dialect, data_mapper=CimDataMapper(options, dialect), default=True)
            dialect = 'car'
            self.add_dialect(dialect, data_mapper=CarDataMapper(options, dialect), default=False, default_include=False)