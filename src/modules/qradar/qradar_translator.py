# Module to handle QRadar conversion
import logging
from stix2patterns_translator.parser import generate_query
from . import aql_query_constructor
from . import qradar_data_mapping

logger = logging.getLogger(__name__)


class QRadarTranslator:

    def stix_to_aql(self, pattern: str) -> str:

        logger.info("Converting STIX2 Pattern to ariel")
        query_object = generate_query(pattern)
        data_model_mapper = qradar_data_mapping.QRadarDataMapper()
        query_string = aql_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string

    def qradar_to_stix(self, qradar_query_results):
        return "QRadar events as STIX observables in JSON format"
