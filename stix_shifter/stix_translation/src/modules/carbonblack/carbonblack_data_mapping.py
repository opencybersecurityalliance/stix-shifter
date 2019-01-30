from os import path
import json
from ...exceptions import DataMappingException


class CarbonBlackDataMapper:
    def __init__(self, options, dialect):
        self.mapping_json = options['mapping'] if 'mapping' in options else {}
        self.select_fields_json = options['select_fields'] if 'select_fields' in options else {}
        self.dialect = dialect

    def _fetch_mapping(self):

        if self.dialect == "process":
            filename = "process_api_from_stix_map.json"
        elif self.dialect == "binary":
            filename = "binary_api_from_stix_map.json"
        else:
            raise RuntimeError("Invalid CarbonBlack dialect: {}".format(self.dialect))

        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "json", filename))
        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data


    def map_field(self, stix_object_name, stix_property_name):
        self.map_data = self.mapping_json or self._fetch_mapping()
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into cb".format(
                stix_object_name, stix_property_name))
