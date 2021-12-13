"""
Parses ANTLR parsing to STIX pattern and invokes custom query_constructor for formatting into native format.

See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md
"""

import logging

from stix_shifter_utils.modules.base.stix_translation.base_query_translator import (
    BaseQueryTranslator
)

from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):
    """
    Class that handles the parsing of the ANTLR parsing and invoking query_constructor to translate to native query.
    """
    def transform_antlr(self, data, antlr_parsing_object):
        """
        Transforms stix pattern to native query.

        :param data: request metadata, not needed for translation
        :type data: map
        :param antlr_parsing_object: STIX pattern to parse
        :type antlr_parsing_object: Pattern
        :return: list of queries
        :rtype: list
        """
        logger.info("Converting STIX2 Pattern to data source query")
        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)

        return query_string
