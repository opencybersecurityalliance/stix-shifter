from abc import ABCMeta, abstractmethod
from os import path
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json


class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, options, dialect, basepath):
        self.options = options
        self.dialect = dialect
        self.map_data = {}
        self.select_fields = {}
        self.logger = logger.set_logger(__name__)
        self.map_data = self.fetch_mapping(basepath, dialect, options)

    def fetch_mapping(self, basepath, dialect, options):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        from_stix_path = path.join(basepath, 'json', f'{dialect}_from_stix_map.json')
        if path.isfile(from_stix_path):
            return read_json(from_stix_path, options)
        else:
            from_stix_path = path.join(basepath, 'json', 'from_stix_map.json')
            return read_json(from_stix_path, options)

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

    def get_language(self):
        return 'stix'
