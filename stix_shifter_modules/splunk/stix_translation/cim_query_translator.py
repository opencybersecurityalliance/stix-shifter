from stix_shifter_utils.modules.cim.stix_translation.query_translator import CimBaseQueryTranslator
import logging
from . import query_constructor

logger = logging.getLogger(__name__)

DEFAULT_SEARCH_KEYWORD = "search"
DEFAULT_FIELDS = "src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol"

class CimQueryTranslator(CimBaseQueryTranslator):

    def transform_query(self, data, antlr_parsing_object):
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

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, DEFAULT_SEARCH_KEYWORD, translate_options)
        return query_string
