from stix_shifter_utils.modules.car.stix_translation.query_translator import CarBaseQueryTranslator
import logging
from . import query_constructor

logger = logging.getLogger(__name__)


class CarQueryTranslator(CarBaseQueryTranslator):

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

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self)
        return query_string
