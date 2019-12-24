from os import path
import glob
import json
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper


class DataMapper(BaseDataMapper):

    def __init__(self, options):
        mapping_json = options['mapping'] if 'mapping' in options else {}
        basepath = path.dirname(__file__)
        self.from_stix_files_cnt = self.json_files_to_fetch(path.abspath(
            path.join(basepath, "json", "from_*.json")))
        self.map_data = mapping_json or self.fetch_mapping()


    @staticmethod
    def json_files_to_fetch(file_path):
        return glob.glob(file_path)

    def fetch_mapping(self):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        map_data = {}
        try:
            for each_file in self.from_stix_files_cnt:
                map_file = open(each_file).read()
                map_data[path.basename(each_file)] = json.loads(map_file)
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

