import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import carbonblack_data_mapping
from . import carbonblack_query_constructor

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5


class StixToCB(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into cbquery query format. Based on a mapping file
        :param data: STIX query string to transform into cbquery query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into cbquery format. This defaults to the from_stix_map.json in the stix_shifter/src/modules/carbonblack/json/ directory
        :type mapping: str (filepath)
        :return: cbquery query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to cbquery")

        query_object = generate_query(data)
        data_model_mapper = carbonblack_data_mapping.CarbonBlackDataMapper(options)
        result_limit = options['result_limit'] if 'result_limit' in options else DEFAULT_LIMIT
        timerange = options['timerange'] if 'timerange' in options else DEFAULT_TIMERANGE
        query_string = carbonblack_query_constructor.translate_pattern(
            query_object, data_model_mapper, result_limit, timerange=timerange)
        return query_string
