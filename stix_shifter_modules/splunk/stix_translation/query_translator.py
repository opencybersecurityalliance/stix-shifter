from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
import logging
from . import query_constructor
from stix_shifter_utils.utils.file_helper import read_json

logger = logging.getLogger(__name__)

DEFAULT_SEARCH_KEYWORD = "search"
DEFAULT_FIELDS = "src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol"

class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        self.select_fields = read_json(f"select_fields", options)

    def transform_antlr(self, data, antlr_parsing_object):
        """
        Transforms STIX pattern into a different query format. Based on a mapping file
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to Splunk query")

        translate_options = {}
        translate_options['result_limit'] = self.options['result_limit']
        time_range = self.options['time_range']
        # append '-' as prefix and 'minutes' as suffix in time_range to convert minutes in SPL query format
        time_range = '-' + str(time_range) + 'minutes'
        translate_options['time_range'] = time_range
        translate_options['index'] = self.options.get('index')

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, DEFAULT_SEARCH_KEYWORD, translate_options)
        return query_string

    def map_object(self, stix_object_name):
        if stix_object_name in self.map_data and self.map_data[stix_object_name] != None:
            return self.map_data[stix_object_name]["cim_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CIM".format(stix_object_name))
