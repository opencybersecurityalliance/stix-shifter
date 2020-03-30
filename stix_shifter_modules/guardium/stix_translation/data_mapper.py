from os import path
import json
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter_utils.modules.base.stix_translation.base_data_mapper import BaseDataMapper

class DataMapper(BaseDataMapper):

    def __init__(self, options, dialect=None):
        super().__init__(dialect)
        mapping_json = options['mapping'] if 'mapping' in options else {}
        basepath = path.dirname(__file__)
        self.map_data = mapping_json or self.fetch_mapping(basepath)

