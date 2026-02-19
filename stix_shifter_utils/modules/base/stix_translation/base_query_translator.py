from abc import ABCMeta
from os import path
import re
import json
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json as helper_read_json
from stix_shifter_utils.stix_translation.src.patterns.parser import generate_query
from stix_shifter_utils.stix_translation.src.utils.stix_pattern_parser import parse_stix
from stix_shifter_utils.stix_translation.src.utils.unmapped_attribute_stripper import strip_unmapped_attributes
from stix2patterns.validator import run_validator
from stix_shifter_utils.stix_translation.src.utils.exceptions import StixValidationException

START_STOP_PATTERN = r"\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d{1,3})?Z'\s?"



class BaseQueryTranslator(object, metaclass=ABCMeta):

    def __init__(self, options, dialect, basepath):
        self.options = options
        self.dialect = dialect
        self.map_data = {}
        self.map_operator = {}
        self.select_fields = {}
        self.logger = logger.set_logger(__name__)
        self.map_data = self.fetch_mapping(basepath, dialect, options)
        self.map_operator = self.fetch_operators(basepath, dialect, options)

    def read_json(self, filepath, options):
        return helper_read_json(filepath, options)
    
    def fetch_operators(self, basepath, dialect, options):
        operator_directory_path = path.join(basepath, 'json')
        operator_file = f'{dialect}_operators.json'
        operator_file_path = path.join(basepath, 'json', operator_file)
        if not path.isfile(operator_file_path):
            # use default operator file since 'default__operators.json' isn't a real dialect
            operator_file = 'operators.json'
        operator_file_path = path.join(operator_directory_path, operator_file)

        return self.read_json(operator_file_path, options)

    def map_comparator(self):
        return self.map_operator

    def fetch_mapping(self, basepath, dialect, options):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        :param basepath: path of data source translation module
        :type basepath: str
        """
        stix_2_0_mapping_directory_path = path.join(basepath, 'json')
        stix_2_1_mapping_directory_path = path.join(basepath, 'json/stix_2_1')
        mapping_file = f'{dialect}_from_stix_map.json'
        from_stix_path = path.join(basepath, 'json', mapping_file)
        if not path.isfile(from_stix_path):
            # use default mapping file since 'default_stix_map.json' isn't a real dialect
            mapping_file = 'from_stix_map.json'
        if options.get("stix_2.1") and path.isdir(stix_2_1_mapping_directory_path):
            from_stix_path = path.join(stix_2_1_mapping_directory_path, mapping_file)
        else:
            from_stix_path = path.join(stix_2_0_mapping_directory_path, mapping_file)
        return self.read_json(from_stix_path, options)

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

    def _validate_pattern(self, pattern):
        errors = []
        # Temporary work around since pattern validator currently treats multiple qualifiers of the same type as invalid.
        start_stop_count = len(re.findall(START_STOP_PATTERN, pattern))
        if(start_stop_count > 1):
            pattern = re.sub(START_STOP_PATTERN, " ", pattern)
        errors = run_validator(pattern, stix_version='2.1')
        if errors:
            raise StixValidationException("The STIX pattern has the following errors: {}".format(errors))

    def parse_query(self, data):
        if self.options.get('validate_pattern'):
            self._validate_pattern(data)
        antlr_parsing = generate_query(data)
        # Extract pattern elements into parsed stix object
        parsed_stix_dictionary = parse_stix(antlr_parsing, self.options['time_range'])
        parsed_stix = parsed_stix_dictionary['parsed_stix']
        start_time = parsed_stix_dictionary['start_time']
        end_time = parsed_stix_dictionary['end_time']
        return {'parsed_stix': parsed_stix, 'start_time': start_time, 'end_time': end_time}

    def transform_query(self, data):
        antlr_parsing = None
        unmapped_stix_collection = []
        unmapped_operator_collection = []
        translated_queries = []
        # if query_translator.get_language() == 'stix':
        if self.options.get('validate_pattern'):
            self._validate_pattern(data)
        antlr_parsing = generate_query(data)
        stripped_parsing = strip_unmapped_attributes(antlr_parsing, self)
        antlr_parsing = stripped_parsing.get('parsing')
        unmapped_stix = stripped_parsing.get('unmapped_stix')
        unmapped_operator = stripped_parsing.get('unmapped_operator')
        if unmapped_stix:
            unmapped_stix_collection.extend(unmapped_stix)
            self.logger.warn(f"The following STIX fields are not supported : {set(unmapped_stix_collection)} with dialect {self.dialect}. The request will ignore those fields. This can result in results that do not match the request.")
        if unmapped_operator:
            unmapped_operator_collection.extend(unmapped_operator)
            self.logger.warn(f"The following STIX operators are not supported : {set(unmapped_operator_collection)} with dialect {self.dialect}. The request will ignore those fields. This can result in results that do not match the request.")
        if antlr_parsing:
            translated_queries = self.transform_antlr(data, antlr_parsing)
            if isinstance(translated_queries, str):
                translated_queries = [translated_queries]
        return {'queries': translated_queries, 'unmapped_attributes': unmapped_stix_collection, 
                "unmapped_operator": unmapped_operator_collection}

    def transform_antlr(self, data, antlr_parsing_object):
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
