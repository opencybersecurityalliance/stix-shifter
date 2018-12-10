import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import bigfix_data_mapping
from . import bigfix_query_constructor

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5


class StixToRelevanceQuery(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into Relevance query format. Based on a mapping file
        :param data: STIX query string to transform into aql query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into aql format. This defaults to the from_stix_map.json in the stix_shifter/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: aql query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to Relevance language")

        query_object = generate_query(data)
        data_model_mapper = bigfix_data_mapping.BigFixDataMapper(options)
        result_limit = options['result_limit'] if 'result_limit' in options else DEFAULT_LIMIT
        timerange = options['timerange'] if 'timerange' in options else DEFAULT_TIMERANGE
        query_string = bigfix_query_constructor.translate_pattern(
            query_object, data_model_mapper, result_limit, timerange)
            
        print(query_string)

        return query_string
