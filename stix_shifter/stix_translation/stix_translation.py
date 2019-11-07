import importlib
from stix_shifter.stix_translation.src.patterns.parser import generate_query
from stix2patterns.validator import run_validator
from stix_shifter.stix_translation.src.utils.stix_pattern_parser import parse_stix
import re
from ..utils.error_response import ErrorResponder
from .src.utils.exceptions import DataMappingException, StixValidationException, UnsupportedDataSourceException, TranslationResultException
from stix_shifter.stix_translation.src.modules.cim import cim_data_mapping
from stix_shifter.stix_translation.src.modules.car import car_data_mapping
from stix_shifter.stix_translation.src.utils.unmapped_attribute_stripper import strip_unmapped_attributes
import sys
TRANSLATION_MODULES = ['qradar', 'dummy', 'car', 'cim', 'splunk', 'elastic', 'bigfix', 'csa', 'csa:at', 'csa:nf', 'aws_security_hub', 'carbonblack', 'elastic_ecs', 'proxy', 'stix_bundle', 'msatp', 'security_advisor']

RESULTS = 'results'
QUERY = 'query'
PARSE = 'parse'
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
START_STOP_PATTERN = "\s?START\s?t'\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z'\sSTOP\s?t'\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}.\d{1,3}Z'\s?"
SHARED_DATA_MAPPERS = {'elastic': car_data_mapping, 'splunk': cim_data_mapping, 'cim': cim_data_mapping, 'car': car_data_mapping}


class StixTranslation:
    """
    StixShifter class - implements translations of stix data
    """

    def __init__(self):
        self.args = []

    def _validate_pattern(self, pattern):
        # Validator doesn't support START STOP qualifier so strip out before validating pattern
        pattern_without_start_stop = re.sub(START_STOP_PATTERN, " ", pattern)
        errors = run_validator(pattern_without_start_stop)
        if (errors != []):
            raise StixValidationException("The STIX pattern has the following errors: {}".format(errors))

    def translate(self, module, translate_type, data_source, data, options={}, recursion_limit=1000):
        """
        Translated queries to a specified format
        :param module: What module to use
        :type module: one of TRANSLATION_MODULES 'qradar', 'dummy'
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
        dialect = None
        mod_dia = module.split(':', 1)
        module = mod_dia[0]
        if len(mod_dia) > 1:
            dialect = mod_dia[1]

        try:
            if module not in TRANSLATION_MODULES:
                raise UnsupportedDataSourceException("{} is an unsupported data source.".format(module))

            translator_module = importlib.import_module(
                "stix_shifter.stix_translation.src.modules." + module + "." + module + "_translator")

            if dialect is not None:
                interface = translator_module.Translator(dialect=dialect)
                options['dialect'] = dialect
            else:
                interface = translator_module.Translator()

            if translate_type == QUERY or translate_type == PARSE:
                # Increase the python recursion limit to allow ANTLR to parse large patterns
                current_recursion_limit = sys.getrecursionlimit()
                if current_recursion_limit < recursion_limit:
                    print("Changing Python recursion limit from {} to {}".format(current_recursion_limit, recursion_limit))
                    sys.setrecursionlimit(recursion_limit)
                options['result_limit'] = options.get('resultSizeLimit', DEFAULT_LIMIT)
                options['timerange'] = options.get('timeRange', DEFAULT_TIMERANGE)
                if translate_type == QUERY:
                    if 'validate_pattern' in options and options['validate_pattern'] == "true":
                        self._validate_pattern(data)
                    try:
                        data_model = importlib.import_module("stix_shifter.stix_translation.src.modules." + module + ".data_mapping")
                        data_model_mapper = data_model.DataMapper(options)
                    except Exception as ex:
                        data_model_mapper = self._cim_or_car_data_mapper(module, options)
                    antlr_parsing = generate_query(data)
                    if data_model_mapper:
                        # Remove unmapped STIX attributes from antlr parsing
                        antlr_parsing = strip_unmapped_attributes(antlr_parsing, data_model_mapper)
                    # Converting STIX pattern to datasource query
                    queries = interface.transform_query(data, antlr_parsing, data_model_mapper, options)
                    return {'queries': queries}
                else:
                    self._validate_pattern(data)
                    # Translating STIX pattern to antlr query object
                    antlr_parsing = generate_query(data)
                    # Extract pattern elements into parsed stix object
                    parsed_stix_dictionary = parse_stix(antlr_parsing, options['timerange'])
                    parsed_stix = parsed_stix_dictionary['parsed_stix']
                    start_time = parsed_stix_dictionary['start_time']
                    end_time = parsed_stix_dictionary['end_time']
                    return {'parsed_stix': parsed_stix, 'start_time': start_time, 'end_time': end_time}

            elif translate_type == RESULTS:
                # Converting data from the datasource to STIX objects
                try:
                    return interface.translate_results(data_source, data, options)
                except Exception:
                    raise TranslationResultException()
            else:
                raise NotImplementedError('wrong parameter: ' + translate_type)
        except Exception as ex:
            print('Caught exception: ' + str(ex) + " " + str(type(ex)))
            response = dict()
            ErrorResponder.fill_error(response, message_struct={'exception': ex})
            return response

    def _cim_or_car_data_mapper(self, module, options):
        if options.get('data_mapper'):
            return SHARED_DATA_MAPPERS[options.get('data_mapper')].mapper_class(options)
        elif module in SHARED_DATA_MAPPERS:
            return SHARED_DATA_MAPPERS[module].mapper_class(options)
        else:
            return None
