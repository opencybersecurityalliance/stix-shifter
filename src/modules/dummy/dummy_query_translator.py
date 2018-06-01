
from ..base.base_query_translator import BaseQueryTranslator


class DummyQueryTranslator(BaseQueryTranslator):

    def transform_query(self, data, mapping=None):
        # transform query...
        return data
