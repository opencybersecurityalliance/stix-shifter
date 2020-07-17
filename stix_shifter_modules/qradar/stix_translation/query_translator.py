from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
import logging
from os import path
import json
from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        if not self.select_fields:
            basepath = path.dirname(__file__)
            aql_fields_json = f"aql_{self.dialect}_fields.json"
            filepath = path.abspath(path.join(basepath, "json", aql_fields_json))
            aql_fields_file = open(filepath).read()
            self.select_fields = json.loads(aql_fields_file)

    def map_selections(self):
        return ", ".join(self.select_fields['default'])

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

        logger.info("Converting STIX2 Pattern to ariel")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)
        return query_string
