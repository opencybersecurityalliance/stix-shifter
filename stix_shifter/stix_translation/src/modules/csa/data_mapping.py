from os import path
import json
import re

from stix_shifter.stix_translation.src.utils.exceptions import DataMappingException

def _fetch_mapping(dialect=''):
    try:
        if dialect != '':
            dialect = dialect + '_'
        basepath = path.dirname(__file__)
        filepath = path.abspath(
            path.join(basepath, "json", dialect + "from_stix_map.json"))

        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data
    except Exception as ex:
        print('exception in main():', ex)
        return {}


class DataMapper:
    def __init__(self, options):
        dialect = options.get('dialect', None)
        if dialect is None:
            self.dialect = 'at'
        else:
            m = re.match(r'^[a-z0-9]+$', dialect)
            if m:
                self.dialect = dialect
            else:
                self.dialect = 'at'

    def map_object(self, stix_object_name):
        self.map_data = _fetch_mapping(self.dialect)
        if stix_object_name in self.map_data and self.map_data[stix_object_name] != None:
            return self.map_data[stix_object_name]
        else:
            raise DataMappingException(
                "Unable to map object `{}` into SQL".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        self.map_data = _fetch_mapping(self.dialect)
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []

    def map_selections(self):
        try:
            basepath = path.dirname(__file__)
            filepath = path.abspath(
                path.join(basepath, "json", self.dialect + "_event_fields.json"))
            sql_fields_file = open(filepath).read()
            sql_fields_json = json.loads(sql_fields_file)

            # Temporary default selections, this will change based on upcoming config override and the STIX pattern that is getting converted to SQL.
            field_list = sql_fields_json['default']
            sql_select = ", ".join(field_list)
            return sql_select
        except Exception as ex:
            print('Exception while reading sql fields file:', ex)
            return {}
