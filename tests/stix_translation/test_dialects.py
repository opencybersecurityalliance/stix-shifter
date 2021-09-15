from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.module_discovery import modules_list

translation = stix_translation.StixTranslation()


class TestTranslationDialecs(object):

    def test_supported_dialects(self):
        modules = modules_list()
        for module in modules:
            result = translation.translate(module, stix_translation.DIALECTS, None, None)
            for dialect, data in result.items():
                assert len(data) == 2
                assert 'language' in data
                assert 'default' in data
