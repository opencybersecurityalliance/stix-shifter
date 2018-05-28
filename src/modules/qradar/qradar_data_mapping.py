import json


def _fetch_mapping():
    try:
        map_file = open(
            'src/modules/qradar/from_stix_map.json').read()
        map_data = json.loads(map_file)
        return map_data
    except Exception as ex:
        print('exception in main():', ex)
        return {}


class DataMappingException(Exception):
    pass


class QRadarDataMapper:

    def map_object(self, stix_object_name):
        self.map_data = _fetch_mapping()
        if stix_object_name in self.map_data and self.map_data[stix_object_name] != None:
            return self.map_data[stix_object_name]
        else:
            raise DataMappingException(
                "Unable to map object `{}` into AQL".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        self.map_data = _fetch_mapping()
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into AQL".format(
                stix_object_name, stix_property_name))
