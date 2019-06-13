from os import path
import json
import re

from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):
    def __init__(self, options):
        if options['dialect'] is None:
            self.dialect = 'at'
        else:
            m = re.match(r'^[a-z0-9]+$', options['dialect'])
            if m:
                self.dialect = options['dialect']
            else:
                self.dialect = 'at'

    def map_field(self, stix_object_name, stix_property_name):
        basepath = path.dirname(__file__)
        self.map_data = self.fetch_mapping(basepath)
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
