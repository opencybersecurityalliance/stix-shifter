from os import path
import json
from stix_shifter.src.exceptions import DataMappingException


def _fetch_mapping():
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


class DummyDataMapper:

    def __init__(self, options):
        mapping_json = options['mapping'] if 'mapping' in options else {}
        self.map_data = mapping_json or _fetch_mapping()

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into data source query".format(
                stix_object_name, stix_property_name))
