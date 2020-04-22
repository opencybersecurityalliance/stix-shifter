from stix_shifter_utils.modules.base.stix_translation.base_data_mapper import BaseDataMapper

class DataMapper(BaseDataMapper):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
