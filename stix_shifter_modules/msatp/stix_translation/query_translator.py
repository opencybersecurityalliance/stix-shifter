import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def transform_antlr(self, data, antlr_parsing_object):
        """
        Transforms STIX query into KQL query format. Based on a mapping file
        :param data: STIX query string to transform into kql query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into
        KQL. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/msatp/json/
        directory
        :type mapping: str (filepath)
        :return: kql query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to KQL query")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)
        return query_string
