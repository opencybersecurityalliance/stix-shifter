from os import path
import json

def _fetch_mapping(mapping=None):
    try:
        basepath = path.dirname(__file__)
        if mapping is None:
            mapping = "from_stix_map.json"
        filepath = path.abspath(
            path.join(basepath, "json", mapping))

        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data
    except Exception as ex:
        print('exception in main():', ex)
        return {}

class DataMappingException(Exception):
    pass

class MongoDataMapper:
    def __init__(self, mapping=None):
        self.map_data = _fetch_mapping(mapping)
    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into Mongo".format(
                stix_object_name, stix_property_name))

