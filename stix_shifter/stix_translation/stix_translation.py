import importlib
import sys
import re
import traceback
from datetime import datetime, timedelta
from stix2patterns.validator import run_validator
from stix_shifter_utils.stix_translation.src.patterns.parser import generate_query
from stix_shifter_utils.stix_translation.src.utils.stix_pattern_parser import parse_stix
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException, StixValidationException, \
    UnsupportedDataSourceException, UnsupportedLanguageException
from stix_shifter_utils.stix_translation.src.utils.unmapped_attribute_stripper import strip_unmapped_attributes
from stix_shifter_utils.utils.module_discovery import process_dialects
from stix_shifter_utils.modules.base.stix_translation.empty_query_translator import EmptyQueryTranslator
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils.param_validator import param_validator
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.logger import exception_to_string

RESULTS = 'results'
QUERY = 'query'
PARSE = 'parse'
MAPPING = 'mapping'
DIALECTS = 'dialects'
SUPPORTED_ATTRIBUTES = "supported_attributes"
START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"
DEFAULT_DIALECT = 'default'


class StixTranslation:
    """
    StixShifter class - implements translations of stix data
    """

    def __init__(self):
        self.args = []
        self.logger = logger.set_logger(__name__)

    def _validate_pattern(self, pattern):
        errors = []
        # Temporary work around since pattern validator currently treats multiple qualifiers of the same type as invalid.
        start_stop_count = len(re.findall(START_STOP_PATTERN, pattern))
        if(start_stop_count > 1):
            pattern = re.sub(START_STOP_PATTERN, " ", pattern)
        errors = run_validator(pattern, stix_version='2.1')
        if (errors):
            raise StixValidationException("The STIX pattern has the following errors: {}".format(errors))
    
    def parse_aql(self, data):
        start_stop_patterns = {
            "\s?START\s?'(\d{4}(-\d{2}){2}\s?(\d{2}:\d{2}))'\s?STOP\s?'(\d{4}(-\d{2}){2}\s?(\d{2}:\d{2}))'": "%Y-%m-%d %H:%M",
            "\s?START\s?'(\d{4}(-\d{2}){2}\s?\d{2}(:\d{2}){2})'\s?STOP\s?'(\d{4}(-\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y-%m-%d %H:%M:%S",
            "\s?START\s?'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'\s?STOP\s?'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y/%m/%d %H:%M:%S",
            "\s?START\s?'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'\s?STOP\s?'(\d{4}(/\d{2}){2}\s?\d{2}(:\d{2}){2})'": "%Y/%m/%d-%H:%M:%S",
            "\s?START\s?'(\d{4}(:\d{2}){2}-\d{2}(:\d{2}){2})'\s?STOP\s?'(\d{4}(:\d{2}){2}-\d{2}(:\d{2}){2})'": "%Y:%m:%d-%H:%M:%S"
        }

        last_time_criteria = "\s?LAST\s?(\d*)\s?(MINUTES|HOURS|DAYS)"

        match = re.search(last_time_criteria, data, re.IGNORECASE)
        if match:
            time_value = match.group(1)
            interval_value = match.group(2)

            current_time = datetime.now()
            if interval_value == 'MINUTES'.lower():
                before_time = current_time - timedelta(minutes=int(time_value))
            elif interval_value == 'HOURS'.lower():
                before_time = current_time - timedelta(hours=int(time_value))
            elif interval_value == 'DAYS'.lower():
                before_time = current_time - timedelta(days=int(time_value))
            
            start_dt_obj = datetime.strptime(str(before_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
            start_time = int(float(start_dt_obj)*1000)

            stop_dt_obj = datetime.strptime(str(current_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%s.%f')
            stop_time = int(float(stop_dt_obj)*1000)
        else:
            for key, value in start_stop_patterns.items():
                match = re.search(key, data, re.IGNORECASE)
                if match:
                    start = match.group(1)
                    stop = match.group(4)

                    str_time = datetime.strptime(start, value).strftime('%s.%f')
                    start_time = int(float(str_time)*1000)
                    stp_time = datetime.strptime(stop, value).strftime('%s.%f')
                    stop_time = int(float(stp_time)*1000)
        return {'start_time': start_time, 'end_time': stop_time}


    def translate(self, module, translate_type, data_source, data, options={}, recursion_limit=1000):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of connector modules: 'qradar', 'dummy'
        :param translate_type: translation of a query or result set must be one of: 'parse', 'mapping' 'query', 'results'
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
                if not translate_type == DIALECTS:
                    validated_options = param_validator(module, options, 'connection.options')
                else:
                    validated_options = {}
                entry_point = connector_module.EntryPoint(options=validated_options)
            except Exception as ex:
                track = traceback.format_exc()
                self.logger.error(ex)
                self.logger.debug(track)
                raise

            if translate_type == DIALECTS:
                dialects = entry_point.get_dialects_full()
                return dialects

            language = validated_options['language']
            if len(dialects) == 0:
                dialects = entry_point.get_dialects(language != 'stix')

            if translate_type == QUERY or translate_type == PARSE:
                # Increase the python recursion limit to allow ANTLR to parse large patterns
                current_recursion_limit = sys.getrecursionlimit()
                if current_recursion_limit < recursion_limit:
                    self.logger.debug("Changing Python recursion limit from {} to {}".format(current_recursion_limit, recursion_limit))
                    sys.setrecursionlimit(recursion_limit)

                if translate_type == QUERY:
                    # Carbon Black combines the mapping files into one JSON using process and binary keys.
                    # The query constructor has some logic around which of the two are used.
                    queries = []
                    unmapped_stix_collection = []
                    dialects_used = 0
                    for dialect in dialects:
                        query_translator = entry_point.get_query_translator(dialect)
                        if not query_translator.get_language() or language == query_translator.get_language():
                            dialects_used += 1
                            antlr_parsing = None
                            if query_translator.get_language() == 'stix':
                                if validated_options.get('validate_pattern'):
                                    self._validate_pattern(data)
                                antlr_parsing = generate_query(data)
                                if query_translator and not isinstance(query_translator, EmptyQueryTranslator):
                                    stripped_parsing = strip_unmapped_attributes(antlr_parsing, query_translator)
                                    antlr_parsing = stripped_parsing.get('parsing')
                                    unmapped_stix = stripped_parsing.get('unmapped_stix')
                                    if unmapped_stix:
                                        unmapped_stix_collection.append(unmapped_stix)
                                    if not antlr_parsing:
                                        continue
                            translated_queries = entry_point.transform_query(dialect, data, antlr_parsing)
                            if isinstance(translated_queries, str):
                                translated_queries = [translated_queries]
                            for query in translated_queries:
                                queries.append(query)
                    if not dialects_used:
                        raise UnsupportedLanguageException(language)
                    if not queries:
                        raise DataMappingException(
                            "{} {}".format(MAPPING_ERROR, unmapped_stix_collection)
                        )
                    return {'queries': queries}
                else:
                    if validated_options.get('language') == 'stix':
                        self._validate_pattern(data)
                        antlr_parsing = generate_query(data)
                        # Extract pattern elements into parsed stix object
                        parsed_stix_dictionary = parse_stix(antlr_parsing, validated_options['time_range'])
                        parsed_stix = parsed_stix_dictionary['parsed_stix']
                        start_time = parsed_stix_dictionary['start_time']
                        end_time = parsed_stix_dictionary['end_time']
                        return {'parsed_stix': parsed_stix, 'start_time': start_time, 'end_time': end_time}
                    else:
                        return self.parse_aql(data)
            elif translate_type == RESULTS:
                # Converting data from the datasource to STIX objects
                return entry_point.translate_results(data_source, data)
            elif translate_type == MAPPING:
                mappings = entry_point.get_mapping()
                return mappings
            elif translate_type == SUPPORTED_ATTRIBUTES:
                # Return mapped STIX attributes supported by the data source
                result = {}
                for dialect in dialects:
                    query_translator = entry_point.get_query_translator(dialect)
                    result[dialect] = query_translator.map_data
                return {'supported_attributes': result}
            else:
                raise NotImplementedError('wrong parameter: ' + translate_type)
        except Exception as ex:
            self.logger.error('Caught exception: ' + str(ex) + " " + str(type(ex)))
            self.logger.debug(exception_to_string(ex))
            response = dict()
            ErrorResponder.fill_error(response, message_struct={'exception': ex})
            return response
