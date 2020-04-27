from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator


class QueryTranslator(BaseQueryTranslator):

    # data, antlr_parsing, data_model_mapper, options
    def transform_query(self, data, antlr_parsing, data_model_mapper):
        """
        Takes in passed in query string and returns it
        :param data: query string that gets returned
        :type data: str
        :param mapping: This is unused
        :type mapping: str
        :return: the passed in data
        :rtype: str
        """
        l = []
        l.append(data)
        return l
