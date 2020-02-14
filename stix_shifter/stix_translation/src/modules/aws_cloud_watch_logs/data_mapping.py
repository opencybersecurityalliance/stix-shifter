from os import path
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        basepath = path.dirname(__file__)
        self.dialect = options.get('dialect') or 'guardduty'
        self.map_data = self.fetch_mapping(basepath)


