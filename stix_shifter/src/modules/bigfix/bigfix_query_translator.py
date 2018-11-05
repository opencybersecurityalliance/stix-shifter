import logging

from ..base.base_query_translator import BaseQueryTranslator
from ...patterns.parser import generate_query

logger = logging.getLogger(__name__)

class BigfixQueryTranslator(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Takes in passed in query string and returns it
        :param data: query string that gets returned
        :type data: str
        :param mapping: This is unused
        :type mapping: str
        :return: the passed in data
        :rtype: str
        """
        # transform query...
        logger.info("Converting STIX2 Pattern to ariel")

        query_object = generate_query(data)
        #ADD THE selectors and the mappers selectors for process, files and how hash, filename, map to where clauses
        #data_model_mapper = qradar_data_mapping.QRadarDataMapper(options)
        print(query_object)

        return data
