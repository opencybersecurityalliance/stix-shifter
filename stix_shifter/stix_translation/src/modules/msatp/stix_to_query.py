import logging

from ..base.base_query_translator import BaseQueryTranslator
from . import query_constructor

logger = logging.getLogger(__name__)


class StixToQuery(BaseQueryTranslator):

    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):
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
            antlr_parsing_object, data_model_mapper, options)
        return query_string
