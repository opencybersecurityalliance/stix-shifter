from ..base.base_result_translator import BaseResultTranslator


class BigfixResultTranslator(BaseResultTranslator):

    def translate_results(self, data_source, data, options, mapping=None):
        """
        Takes in passed in results string and returns it
        :param data_source: STIX identity object representing a data source
        :type data_source: str
        :param data: results string that gets returned
        :type data: str
        :param mapping: This is unused
        :type mapping: str
        :return: the passed in data
        :rtype: str
        """
        # translate results...
        return data
