import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def transform_query(self, data, antlr_parsing_object):
        """
        Transforms STIX pattern into a different query format. Based on a mapping file
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
<<<<<<< HEAD
=======
        :data_model_mapper: Mapping object for the data source
        :type data_model_mapper: object
>>>>>>> guard-dev
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to data source query")

        query_string = query_constructor.translate_pattern(
<<<<<<< HEAD
            antlr_parsing_object, self, self.options)
=======
            antlr_parsing_object, data_model_mapper, options)
>>>>>>> guard-dev
        return query_string
