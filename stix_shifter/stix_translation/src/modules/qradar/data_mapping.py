from os import path
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        self.mapping_json = options['mapping'] if 'mapping' in options else {}
        self.select_fields_json = options['select_fields'] if 'select_fields' in options else {}
        basepath = path.dirname(__file__)
        self.dialect = options.get('dialect') or 'events'
        self.map_data = self.mapping_json or self.fetch_mapping(basepath)

    def map_selections(self):
        try:
            if self.select_fields_json:
                aql_fields_json = self.select_fields_json
                field_list = aql_fields_json
            else:
                basepath = path.dirname(__file__)
                if self.dialect == 'flows':
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
