from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from stix_shifter_utils.modules.cim.stix_translation.cim_data_mapper import CimDataMapper
from stix_shifter_utils.modules.car.stix_translation.car_data_mapper import CarDataMapper
from .stix_translation.stix_to_elastic  import StixToElastic
class EntryPoint(EntryPointBase):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.add_dialect('default', query_translator=StixToElastic(), data_mapper=CarDataMapper(options), default=True)
        self.add_dialect('cim', query_translator=StixToElastic(), data_mapper=CimDataMapper(options), default_include=False)
        self.add_dialect('car', query_translator=StixToElastic(), data_mapper=CarDataMapper(options), default_include=False)