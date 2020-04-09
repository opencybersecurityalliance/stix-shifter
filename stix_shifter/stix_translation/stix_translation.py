import importlib
from stix_shifter_utils.stix_translation.src.patterns.parser import generate_query
from stix2patterns.validator import run_validator
from stix_shifter_utils.stix_translation.src.utils.stix_pattern_parser import parse_stix
import re
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException, StixValidationException, UnsupportedDataSourceException, TranslationResultException
from stix_shifter_utils.stix_translation.src.utils.unmapped_attribute_stripper import strip_unmapped_attributes
from stix_shifter_utils.utils.module_discovery import process_dialects
import sys
import glob
from os import path
import traceback

RESULTS = 'results'
QUERY = 'query'
PARSE = 'parse'
SUPPORTED_ATTRIBUTES = "supported_attributes"
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"
DEFAULT_DIALECT = 'default'


class StixTranslation:
    """
    StixShifter class - implements translations of stix data
    """

    def __init__(self):
        self.args = []

    def _validate_pattern(self, pattern):
        errors = []
        # Temporary work around since pattern validator currently treats multiple qualifiers of the same type as invalid.
        start_stop_count = len(re.findall(START_STOP_PATTERN, pattern))
        if(start_stop_count > 1):
            pattern = re.sub(START_STOP_PATTERN, " ", pattern)
        errors = run_validator(pattern, stix_version='2.1')
        if (errors):
            raise StixValidationException("The STIX pattern has the following errors: {}".format(errors))


    def translate(self, module, translate_type, data_source, data, options={}, recursion_limit=1000):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of connector modules: 'qradar', 'dummy'
        :param translate_type: translation of a query or result set must be either 'results' or 'query'
        :type translate_type: str
        :param data: the data to translate
        :type data: str
        :param options: translation options { stix_validator: bool }
        :type options: dict
        :param recursion_limit: maximum depth of Python interpreter stack
        :type recursion_limit: int
        :return: translated results
        :rtype: str
        """

        module, dialects = process_dialects(module, options)
        
        try:
            try:
                connector_module = importlib.import_module("stix_shifter_modules." + module + ".entry_point")
            except Exception as ex:
                raise UnsupportedDataSourceException("{} is an unsupported data source.".format(module))
            try: 
                entry_point = connector_module.EntryPoint(options=options)
            except Exception as ex:
                track = traceback.format_exc()
                print(ex)
                print(track) 
                raise                

            if len(dialects) == 0:
                dialects = entry_point.get_dialects()

            if translate_type == QUERY or translate_type == PARSE:
                # Increase the python recursion limit to allow ANTLR to parse large patterns
                current_recursion_limit = sys.getrecursionlimit()
                if current_recursion_limit < recursion_limit:
                    print("Changing Python recursion limit from {} to {}".format(current_recursion_limit, recursion_limit))
                    sys.setrecursionlimit(recursion_limit)
                options['result_limit'] = options.get('resultSizeLimit', DEFAULT_LIMIT)
                options['time_range'] = options.get('timeRange', DEFAULT_TIMERANGE)

                if translate_type == QUERY:
                    # Carbon Black combines the mapping files into one JSON using process and binary keys.
                    # The query constructor has some logic around which of the two are used.
                    if options.get('validate_pattern'):
                        self._validate_pattern(data)
                    queries = []
                    unmapped_stix_collection = []
                    for dialect in dialects:
                        antlr_parsing = generate_query(data)
                        data_model_mapper = entry_point.get_data_mapper(dialect)
                        if data_model_mapper:
                            stripped_parsing = strip_unmapped_attributes(antlr_parsing, data_model_mapper)
                            antlr_parsing = stripped_parsing.get('parsing')
                            unmapped_stix = stripped_parsing.get('unmapped_stix')
                            if unmapped_stix:
                                unmapped_stix_collection.append(unmapped_stix)
                            if not antlr_parsing:
                                continue
                        translated_queries = entry_point.transform_query(dialect, data, antlr_parsing, options)
                        
                        if isinstance(translated_queries, str):
                            translated_queries = [translated_queries]
                        for query in translated_queries:
                            queries.append(query)

                    if not queries:
                        raise DataMappingException(
                            "{} {}".format(MAPPING_ERROR, unmapped_stix_collection)
                        )

                    return {'queries': queries}
                else:
                    self._validate_pattern(data)
                    antlr_parsing = generate_query(data)
                    # Extract pattern elements into parsed stix object
                    parsed_stix_dictionary = parse_stix(antlr_parsing, options['time_range'])
                    parsed_stix = parsed_stix_dictionary['parsed_stix']
                    start_time = parsed_stix_dictionary['start_time']
                    end_time = parsed_stix_dictionary['end_time']
                    return {'parsed_stix': parsed_stix, 'start_time': start_time, 'end_time': end_time}

            elif translate_type == RESULTS:
                # Converting data from the datasource to STIX objects
                return entry_point.translate_results(data_source, data, options)
            elif translate_type == SUPPORTED_ATTRIBUTES:
                # Return mapped STIX attributes supported by the data source
                result = {}
                for dialect in dialects:
                    data_model_mapper = entry_point.get_data_mapper(dialect)
                    result[dialect] = data_model_mapper.map_data
                    
                return {'supported_attributes': result}
            else:
                raise NotImplementedError('wrong parameter: ' + translate_type)
        except Exception as ex:
            print('Caught exception: ' + str(ex) + " " + str(type(ex)))
            response = dict()
            ErrorResponder.fill_error(response, message_struct={'exception': ex})
            return response

