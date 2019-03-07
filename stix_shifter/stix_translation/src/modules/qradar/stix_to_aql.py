import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import qradar_data_mapping
from . import aql_query_constructor

logger = logging.getLogger(__name__)


class StixToAQL(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into aql query format. Based on a mapping file
        :param data: STIX query string to transform into aql query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into aql format. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: aql query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to ariel")

        query_object = generate_query(data)
        data_model_mapper = qradar_data_mapping.QRadarDataMapper(options)
        query_string = aql_query_constructor.translate_pattern(
            query_object, data_model_mapper, options)
        return query_string
