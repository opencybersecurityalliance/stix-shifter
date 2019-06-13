from stix_shifter.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper
from os import path
import json


class CarDataMapper(BaseDataMapper):

    def __init__(self, options={}):
        self.options = options
        mapping_json = options.get('mapping')
        self.MAPPINGS = mapping_json or self.fetch_mapping()

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

    def map_object(self, stix_object_name):
        if self.MAPPINGS.get(stix_object_name):
            return self.MAPPINGS[stix_object_name]["car_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CAR".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.MAPPINGS and stix_property_name in self.MAPPINGS[stix_object_name]["fields"]:
            return self.MAPPINGS[stix_object_name]["fields"][stix_property_name]
        else:
            return []


mapper_class = CarDataMapper
