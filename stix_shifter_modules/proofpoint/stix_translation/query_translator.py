import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
from . import query_constructor
logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

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

        logger.info(f"Converting STIX2 Pattern {data} to data source query")

        """
        Due to Proofpoint SIEM API limitation, the connector cannot query any standard stix object.
        We have added mapping in the from_stix_map.json to avoid throwing mapping error by the connector.
        Connector can only translate stix pattern that includes 'x-proofpoint' custom object.
        
        Below condition is to verify if pattern contains 'x-proofpoint' object if not
        it simply removes all other objects from the mapping except 'x-proofpoint' and print a debug message
        """
        if data not in self.map_data['x-proofpoint']["fields"]:
            logger.debug(f'Proofpoint connector cannot query any STIX objects except only x-proofpoint custom STIX Object' )
            temp_map = {}
            temp_map['x-proofpoint'] = self.map_data['x-proofpoint']
            self.map_data.clear()
            self.map_data = temp_map

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)
        return query_string