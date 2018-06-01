from ..base.base_result_translator import BaseResultTranslator


class DummyResultTranslator(BaseResultTranslator):

    def translate_results(self, data, mapping=None):
        # translate results...
        return data
