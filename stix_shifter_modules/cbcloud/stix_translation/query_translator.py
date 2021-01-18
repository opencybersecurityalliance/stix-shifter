import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from . import query_constructor

LOGGER = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def transform_antlr(self, data, antlr_parsing_object) -> str:
        """Transforms STIX pattern into a Carbon Black Cloud format, based on a
        mapping file.

        :param data: STIX query string to transform into Carbon Black Cloud format
        :type data: str
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :param mapping: The mapping file path to use as instructions on how to
            transform the given STIX query into Carbon Black Cloud format. This
            defaults to the from_stix_map.json in the
            stix_shifter_modules/cbcloud/stix_translation/json/ directory
        :type mapping: str (filepath)
        :return: transformed Carbon Black Cloud query string
        :rtype: str
        """

        LOGGER.info("Converting STIX2 Pattern to Carbon Black Cloud query")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options
        )

        return query_string
