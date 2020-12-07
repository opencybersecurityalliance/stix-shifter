import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        self.transformers = get_module_transformers('guardium')

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

        logger.info("Converting STIX2 Pattern to data source query")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options, self.transformers)        
        return query_string
