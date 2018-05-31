# Module to handle QRadar conversion
import logging
import json
from stix2patterns_translator.parser import generate_query
from . import aql_query_constructor
from . import qradar_data_mapping
from src.json_to_stix import json_to_stix
from src.json_to_stix import transformers

logger = logging.getLogger(__name__)


class QRadarTranslator:

    def stix_to_aql(self, pattern: str) -> str:

        logger.info("Converting STIX2 Pattern to ariel")
        query_object = generate_query(pattern)
        data_model_mapper = qradar_data_mapping.QRadarDataMapper()
        query_string = aql_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string

    def qradar_to_stix(self, qradar_query_results, map=None):

        if(map is None):
            map_file = open('src/modules/qradar/to_stix_map.json').read()
            map_data = json.loads(map_file)
        else:
            map_data = json.loads(map)

        # todo: make datasource id/name dynamic
        datasource = {
            'id': '7c0de425-33bf-46be-9e38-e42319e36d95', 'name': 'events'}

        results = json_to_stix.convert_to_stix(
            datasource, map_data, qradar_query_results, transformers.get_all_transformers())

        return json.dumps(results)
