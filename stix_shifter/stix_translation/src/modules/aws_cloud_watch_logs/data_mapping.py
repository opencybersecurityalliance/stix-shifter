from os import path
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        basepath = path.dirname(__file__)
        self.mapping_file = options.get('mapping_file')
        self.map_data = self.fetch_mapping(basepath)
