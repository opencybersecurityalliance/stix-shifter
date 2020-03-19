from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.dummy_translator import Translator
from .stix_translation.data_mapping import DataMapper

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        self.parent_init(options)
        self.add_dialect('default', Translator(), DataMapper(options), default=True)