import logging

from stix2patterns_translator.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import mongo_data_mapper
from . import mongo_query_constructor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StixToMongo(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into aql query format. Based on a mapping file
        :param data: STIX query string to transform into mongo query object
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into various mongo shemas. This defaults to the from_stix_map.json in the stix_shifter/src/modules/mongo/json/ directory
        :type mapping: str (filepath)
        :return: aql query string
        :rtype: str
        """
        stix_pattern = data

        logger.info("Converting STIX2 Pattern to mongo")

        query_object = generate_query(stix_pattern)
        logger.info("Query: %s", query_object)
        print(query_object.expression)
        data_model_mapper = mongo_data_mapper.MongoDataMapper(mapping)
        query_string = mongo_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string
