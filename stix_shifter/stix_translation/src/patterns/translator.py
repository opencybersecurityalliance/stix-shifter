from stix_shifter.stix_translation import stix_translation
from enum import Enum

class SearchPlatforms(Enum):
    ELASTIC = 'elastic'
    SPLUNK = 'splunk'


class DataModels(Enum):
    CAR = 'car'
    CIM = 'cim'

def translate(pattern: str, search_platform=SearchPlatforms.ELASTIC, data_model=DataModels.CAR):
    options = { 'data_mapper' : data_model.value }
    translation = stix_translation.StixTranslation()
    return translation.translate(
        search_platform.value, stix_translation.QUERY, {}, pattern, options=options)
