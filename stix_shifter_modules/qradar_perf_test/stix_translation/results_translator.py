from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from .qradar_utils import hash_type_lookup

class ResultsTranslator(JSONToStix):

  def __init__(self, options, dialect, base_file_path=None, callback=None):
    super().__init__(options, dialect, base_file_path, hash_type_lookup)
