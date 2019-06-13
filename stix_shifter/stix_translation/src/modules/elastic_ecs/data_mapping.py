from os import path
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        mapping_json = options['mapping'] if 'mapping' in options else {}
        self.map_data = mapping_json or self.fetch_mapping()

    def fetch_mapping(self):
        try:
            basepath = path.dirname(__file__)
            filepath = path.abspath(
                path.join(basepath, "json", "from_stix_map.json"))

            map_file = open(filepath).read()
            map_data = json.loads(map_file)
            return map_data
        except Exception as ex:
            print('exception in main():', ex)
            return {}

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []
