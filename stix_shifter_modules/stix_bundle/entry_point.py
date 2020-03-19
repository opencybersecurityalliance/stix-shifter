from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.stix_bundle_translator import Translator

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        self.parent_init(options)
        self.add_dialect('default', Translator(), None, True)