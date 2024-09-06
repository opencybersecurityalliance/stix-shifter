from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
import logging
from . import query_constructor  # Updated to use the Securonix-specific query constructor
from stix_shifter_utils.utils.file_helper import read_json

logger = logging.getLogger(__name__)

DEFAULT_SEARCH_KEYWORD = "search"
DEFAULT_FIELDS = "destinationaddress"

class SecuronixQueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        self.select_fields = read_json(f"select_fields", options)

    def transform_antlr(self, data, antlr_parsing_object):
        """
        Transforms STIX pattern into a Securonix query format.
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to Securonix query")

        translate_options = {}
        translate_options['result_limit'] = self.options['result_limit']
        time_range = self.options['time_range']
        # Convert time range to the format Securonix expects (assumed to be minutes for simplicity)
        time_range = str(time_range) + 'minutes'
        translate_options['time_range'] = time_range
        translate_options['index'] = self.options.get('index')

        # Use the Securonix query constructor to translate the pattern
        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, DEFAULT_SEARCH_KEYWORD, translate_options)
        return query_string

    def map_object(self, stix_object_name):
        """
        Maps STIX objects to their corresponding Securonix fields.
        """
        if stix_object_name in self.map_data and self.map_data[stix_object_name] is not None:
            return self.map_data[stix_object_name]["securonix_type"]  # Updated to reflect Securonix mapping
        else:
            raise DataMappingException(f"Unable to map object `{stix_object_name}` into Securonix fields")

