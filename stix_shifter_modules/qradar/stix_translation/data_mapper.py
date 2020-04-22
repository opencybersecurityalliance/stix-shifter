from os import path
import json
from stix_shifter_utils.modules.base.stix_translation.base_data_mapper import BaseDataMapper

class DataMapper(BaseDataMapper):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        if not self.select_fields:
            basepath = path.dirname(__file__)
            aql_fields_json = f"aql_{self.dialect}_fields.json"
            filepath = path.abspath(path.join(basepath, "json", aql_fields_json))
            aql_fields_file = open(filepath).read()
            self.select_fields = json.loads(aql_fields_file)

    def map_selections(self):
        return ", ".join(self.select_fields['default'])
