from os import path
from ..base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        mapping_json = options['mapping'] if 'mapping' in options else {}
        basepath = path.dirname(__file__)
        self.map_data = mapping_json or self.fetch_mapping(basepath)
