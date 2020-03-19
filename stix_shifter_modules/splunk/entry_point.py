from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from stix_shifter_utils.modules.cim.stix_translation.cim_data_mapping import CimDataMapper
from stix_shifter_utils.modules.car.stix_translation.car_data_mapping import CarDataMapper
from .stix_translation.splunk_translator import Translator

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        self.parent_init(options)
        self.add_dialect('default', Translator(), CimDataMapper(options), True)
        self.add_dialect('cim', Translator(), CimDataMapper(options), False, default_include=False)
        self.add_dialect('car', Translator(), CarDataMapper(options), False, default_include=False)