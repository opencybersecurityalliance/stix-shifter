from stix_shifter import stix_shifter
from enum import Enum

class SearchPlatforms(Enum):
    ELASTIC = 'elastic'
    SPLUNK = 'splunk'


class DataModels(Enum):
    CAR = 'car'
    CIM = 'cim'

def translate(pattern: str, search_platform=SearchPlatforms.ELASTIC, data_model=DataModels.CAR):
    options = { 'data_mapper' : data_model.value }
    shifter = stix_shifter.StixShifter()
    return shifter.translate(
        search_platform.value, stix_shifter.QUERY, {}, pattern, options=options)
