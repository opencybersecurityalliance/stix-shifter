import logging

from ..base.base_query_translator import BaseQueryTranslator
from . import data_mapping
from . import query_constructor

logger = logging.getLogger(__name__)


class StixToCloudSQL(BaseQueryTranslator):

    def __init__(self, dialect=None, rows=1024):
        super().__init__()
        self.dialect = dialect
        self.rows = rows

    def transform_query(self, data, antlr_parsing_object, data_model_mapper, options, mapping=None):
        """
        Transforms STIX query into sql query format. Based on a mapping file
        :param data: STIX query string to transform into sql query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into sql format. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: sql query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to sql")
        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, data_model_mapper, number_rows=self.rows)
        return query_string
