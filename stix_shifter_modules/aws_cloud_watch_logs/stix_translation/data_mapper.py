from os import path
from stix_shifter_utils.modules.base.stix_translation.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options, dialect='guardduty'):
        super().__init__(dialect)
        basepath = path.dirname(__file__)
        self.map_data = self.fetch_mapping(basepath)


