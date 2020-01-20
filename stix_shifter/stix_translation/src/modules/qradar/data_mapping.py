from os import path
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper
import glob


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        self.select_fields_json = options['select_fields'] if 'select_fields' in options else {}
        basepath = path.dirname(__file__)
        # Relying on file names for mapping keys will make custom mappings difficult; the end user won't know what mapping files are used.
        # See tests/stix_translation/qradar_stix_to_aql/options.json for how it would currently need to be brought in.
        # TODO: Both QRadar and AWS CloudWatch Logs will need to be revisited for custom mapping support.
        # May need to use one mapping file with different keys.
        self.from_stix_files_cnt = self.json_files_to_fetch(path.abspath(path.join(basepath, "json", "from_*.json")))
        self.map_data = self.fetch_mapping(options)

    @staticmethod
    def json_files_to_fetch(file_path):
        return glob.glob(file_path)

    def fetch_mapping(self, options):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        try:
            map_data = options.get('mapping', {})
            if not map_data:
                for each_file in self.from_stix_files_cnt:
                    map_file = open(each_file).read()
                    map_data[path.basename(each_file)] = json.loads(map_file)
                print("USING REGULAR MAPPING {}".format(map_data))
            else:
                print("USING CUSTOM MAPPING {}".format(map_data))
            return map_data
        except Exception as ex:
            print('exception in main():', ex)
            return {}

    def map_field(self, stix_object_name, stix_property_name):
        """
        :param stix_object_name: str, stix object
        :param stix_property_name: str, stix field
        :return: list
        """
        mapped_field_lst = []
        for each_model_mapper in self.map_data.values():
            if stix_object_name in each_model_mapper and stix_property_name in \
                    each_model_mapper[stix_object_name]["fields"]:
                mapped_field_lst.append(each_model_mapper[stix_object_name]["fields"][stix_property_name])
        print("HERE ARE THE MAPPED FIELDS: {}".format(mapped_field_lst))
        return mapped_field_lst

    def map_field_json(self, stix_object_name, stix_property_name, json_file):
        """
        Return mapped fields from json file
        :param stix_object_name:str, stix object
        :param stix_property_name:str, stix field
        :param json_file:str, json file name
        :return: list
        """
        if stix_object_name in self.map_data.get(json_file) and stix_property_name in \
                self.map_data.get(json_file)[stix_object_name]["fields"]:
            return self.map_data.get(json_file)[stix_object_name]["fields"][stix_property_name]
        else:
            return []

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
