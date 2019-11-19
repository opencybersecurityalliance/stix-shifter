
from ..base.base_query_translator import BaseQueryTranslator
from .utils.StixPatternParser import StixPatternParser


class SecurityAdvisorQueryTranslator(BaseQueryTranslator):

    # data, antlr_parsing, data_model_mapper, options
    def transform_query(self, data, antlr_parsing, data_model_mapper ,options={}, mapping=None, ):
        """
        Takes in passed in query string and returns it
        :param data: query string that gets returned
        :type data: str
        :param mapping: This is unused
        :type mapping: str
        :return: the passed in data
        :rtype: str
        """
        result = StixPatternParser().parse(data)
        return result
