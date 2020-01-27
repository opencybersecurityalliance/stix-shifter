from os import path
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        self.select_fields_json = options['select_fields'] if 'select_fields' in options else {}
        basepath = path.dirname(__file__)
        self.mapping_file = options.get('mapping_file')
        self.map_data = self.fetch_mapping(basepath)

    def map_selections(self):
        try:
            if self.select_fields_json:
                aql_fields_json = self.select_fields_json
                field_list = aql_fields_json
            else:
                basepath = path.dirname(__file__)
                if "flow" in self.mapping_file:
                    aql_fields_json = "aql_flow_fields.json"
                else:
                    aql_fields_json = "aql_event_fields.json"
                filepath = path.abspath(path.join(basepath, "json", aql_fields_json))
                aql_fields_file = open(filepath).read()
                aql_fields_json = json.loads(aql_fields_file)
                # Temporary default selections, this will change based on config override and the STIX pattern that is getting converted to AQL.
                field_list = aql_fields_json['default']
            aql_select = ", ".join(field_list)

            return aql_select
        except Exception as ex:
            print('Exception while reading aql fields file:', ex)
            return {}
