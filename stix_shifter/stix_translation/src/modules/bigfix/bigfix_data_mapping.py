from os import path
import json
from stix_shifter.stix_translation.src.exceptions import DataMappingException


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


class BigFixDataMapper:

    def __init__(self, options):
        self.mapping_json = options['mapping'] if 'mapping' in options else {}
        self.select_fields_json = options['select_fields'] if 'select_fields' in options else {}

    def map_field(self, stix_object_name, stix_property_name, stix_key_name):
        self.map_data = self.mapping_json or _fetch_mapping()
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
           return self.map_data[stix_object_name]["fields"][stix_property_name][0]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into Relevance reference".format(
                stix_object_name, stix_property_name))

    def map_selections(self):
        try:
            if self.select_fields_json:
                aql_fields_json = self.select_fields_json
                field_list = aql_fields_json
            else:
                basepath = path.dirname(__file__)
                filepath = path.abspath(
                    path.join(basepath, "json", "aql_event_fields.json"))
                aql_fields_file = open(filepath).read()
                aql_fields_json = json.loads(aql_fields_file)
                # Temporary default selections, this will change based on config override and the STIX pattern that is getting converted to AQL.
                field_list = aql_fields_json['default']
            aql_select = ", ".join(field_list)

            return aql_select
        except Exception as ex:
            print('Exception while reading aql fields file:', ex)
            return {}
