import logging

from stix2patterns_translator.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import qradar_data_mapping
from . import aql_query_constructor

logger = logging.getLogger(__name__)


class StixToAQL(BaseQueryTranslator):

    def transform_query(self, data, mapping=None):
        # if translating STIX pattern to AQL...
        stix_pattern = data

        logger.info("Converting STIX2 Pattern to ariel")

        query_object = generate_query(stix_pattern)
        data_model_mapper = qradar_data_mapping.QRadarDataMapper()
        query_string = aql_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string
