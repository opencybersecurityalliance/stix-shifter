import logging

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import data_mapping
from . import query_constructor

logger = logging.getLogger(__name__)


class StixToQuery(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into data source query format. Based on a mapping file
        :param data: STIX query string to transform into data source query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into data source query format.
        :type mapping: str (filepath)
        :return: data source query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to data source query")

        query_object = generate_query(data)
        data_model_mapper = data_mapping.DataMapper(options)

        query_string = query_constructor.translate_pattern(
            query_object, data_model_mapper, options)
        return query_string
