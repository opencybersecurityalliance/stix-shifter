from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator


class AqlQueryTranslator(BaseQueryTranslator):

    def get_language(self):
        return 'aql'

    def fetch_mapping(self, basepath, dialect, options):
        pass

    def transform_query(self, data, unused_antlr_parsing_object=None):
        return data
