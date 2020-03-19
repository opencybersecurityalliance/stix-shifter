from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_translation.security_advisor_translator import Translator

class EntryPoint(EntryPointBase):

    def __init__(self, options):
        self.parent_init(options)
        self.add_dialect('default', Translator(), None, True)