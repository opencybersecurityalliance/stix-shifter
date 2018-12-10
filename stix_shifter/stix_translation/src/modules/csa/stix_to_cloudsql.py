import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import cloudsql_data_mapping
from . import cloudsql_query_constructor

logger = logging.getLogger(__name__)


class StixToCloudSQL(BaseQueryTranslator):

    def __init__(self, dialect=None):
        super().__init__()
        self.dialect = dialect

    def transform_query(self, data, options, mapping=None):
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

        query_object = generate_query(data)
        data_model_mapper = cloudsql_data_mapping.CloudSQLDataMapper(self.dialect)
        query_string = cloudsql_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string
