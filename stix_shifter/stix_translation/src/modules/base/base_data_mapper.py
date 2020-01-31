from abc import ABCMeta, abstractmethod
from os import path
import json
import glob


class BaseDataMapper(object, metaclass=ABCMeta):

    def fetch_mapping(self, basepath):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        try:
            if hasattr(self, 'dialect') and not(self.dialect == 'default'):
                filepath = self._fetch_from_stix_mapping_file(basepath)
            else:
                filepath = path.abspath(path.join(basepath, "json", 'from_stix_map.json'))
            map_file = open(filepath).read()
            map_data = json.loads(map_file)
            return map_data
        except Exception as ex:
            print('exception in main():', ex)
            return {}

    def map_field(self, stix_object_name, stix_property_name):
        """
        Maps the STIX object:property pair to any matching data source fields. 
        Mapping is based on a JSON object defined in the data source DataMapper class
        :param stix_object_name: STIX object (ie. url)
        :type stix_object_name: str
        :param stix_property_name: STIX property associated to the object (ie. value)
        :type stix_property_name: str
        :return: A list of 0 or more data source fields that map to a combination of stix_object_name and stix_property_name
        :rtype: list
        """
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []

    def _fetch_from_stix_mapping_file(self, basepath):
        mapping_paths = glob.glob(path.abspath(path.join(basepath, "json", "{}_from_stix*.json".format(self.dialect))))
        return mapping_paths[0]
