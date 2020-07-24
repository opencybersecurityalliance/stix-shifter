from abc import ABCMeta, abstractmethod
from os import path
import json
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter_utils.utils import logger
import glob

class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, options, dialect, basepath):
        self.options = options
        self.dialect = dialect
        self.basepath = basepath #used in tests
        self.map_data = {}
        self.select_fields = {}
        self.logger = logger.set_logger(__name__)

        mapping = options['mapping'] if 'mapping' in options else None
        if mapping and dialect in mapping:
            mapping = mapping[dialect]
            if 'from_stix' in mapping:
                self.map_data = mapping['from_stix']
            if 'select_fields' in mapping:
                self.select_fields = mapping['select_fields']

        if not self.map_data:
            self.map_data = self.fetch_mapping(basepath)

    def get_select_fields(self):
        return self.select_fields

    def fetch_mapping(self, basepath):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        try:
            if hasattr(self, 'dialect') and not(self.dialect == None) and not(self.dialect == 'default'):
                filepath = self.__fetch_from_stix_mapping_file(basepath)
            else:                
                filepath = path.abspath(path.join(basepath, "json", 'from_stix_map.json'))
            map_file = open(filepath).read()
            map_data = json.loads(map_file)
            return map_data
        except Exception as ex:
            self.logger.error('exception in BaseQueryTranslator::fetch_mapping():', ex)
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

    def __fetch_from_stix_mapping_file(self, basepath):
        mapping_paths = glob.glob(path.abspath(path.join(basepath, "json", "{}_from_stix*.json".format(self.dialect))))
        return mapping_paths[0]

    @abstractmethod
    def transform_query(self, data, antlr_parsing_object):
        """
        Transforms STIX pattern into a different query format. Based on a mapping file
        :param data: STIX pattern to transform into native data source query
        :type data: str
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """
        # if translating STIX pattern to a datasource query...
        raise NotImplementedError()
