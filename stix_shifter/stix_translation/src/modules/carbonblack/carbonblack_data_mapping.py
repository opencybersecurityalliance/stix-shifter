from os import path
import json
from ...exceptions import DataMappingException


class CarbonBlackDataMapper:
    def __init__(self, options):
        self.map_data = self._fetch_mappings()

    def _fetch_mappings(self):
        process_mapping = self._fetch_mapping_file("process_api_from_stix_map.json")
        binary_mapping = self._fetch_mapping_file("binary_api_from_stix_map.json")
        return [("binary", binary_mapping), ("process", process_mapping)]

    def _fetch_mapping_file(self, filename):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "json", filename))
        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data

    def map_field(self, stix_object_name, stix_property_name):
        results = []
        for dialect, mapping in self.map_data:
            if stix_object_name in mapping and stix_property_name in mapping[stix_object_name]["fields"]:
                results.append((mapping[stix_object_name]["fields"][stix_property_name], dialect))

        if len(results) != 0:
            return results
        else:
            raise DataMappingException("Unable to map property `{}:{}` into cb".format(
                stix_object_name, stix_property_name))
