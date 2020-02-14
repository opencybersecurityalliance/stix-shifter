from os import path
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):
    def __init__(self, options):
        self.map_data = options.get('mappings', False) or self.fetch_mapping()
        assert len(self.map_data) == 2
        assert "process" in self.map_data and "binary" in self.map_data

    def fetch_mapping(self):
        process_mapping = self._fetch_mapping_file("process_from_stix_map.json")
        binary_mapping = self._fetch_mapping_file("binary_from_stix_map.json")
        return {"binary": binary_mapping, "process": process_mapping}

    def _fetch_mapping_file(self, filename):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "json", filename))
        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data

    def map_field(self, stix_object_name, stix_property_name):
        results = []
        for dialect in ["binary", "process"]:  # binary api fields mappings are preferred
            mapping = self.map_data[dialect]
            if stix_object_name in mapping and stix_property_name in mapping[stix_object_name]["fields"]:
                results.append((mapping[stix_object_name]["fields"][stix_property_name], dialect))

        if len(results) != 0:
            return results
        else:
            return []
