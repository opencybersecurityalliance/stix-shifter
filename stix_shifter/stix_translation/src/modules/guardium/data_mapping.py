from os import path
import json
from stix_shifter.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper

#class DataMapper:
class DataMapper(BaseDataMapper):

    def __init__(self, options):
        mapping_json = options['mapping'] if 'mapping' in options else {}
        basepath = path.dirname(__file__)
        self.map_data = mapping_json or self.fetch_mapping(basepath)

