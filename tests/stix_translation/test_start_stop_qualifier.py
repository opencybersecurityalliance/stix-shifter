from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.module_discovery import modules_list

translation = stix_translation.StixTranslation()
STIX_PATTERN = "[ipv4-addr:value = '192.168.0.100'] START t'2022-11-18T15:00:00Z' STOP t'2022-11-20T16:00:00Z'"


class TestQualifierTimestamps(object):
    translation_errors ={}

    def validate_stix_result(self, result, module):
        if 'error' in result:
            if "timestamp" not in result["error"]:
                next
            else:
                self.translation_errors[module] = result['error']

    def test_supported_dialects(self):
        
        modules = modules_list()
        for module in modules:
            result = translation.translate(module, 'query', '', STIX_PATTERN, {})
            self.validate_stix_result(result, module)
        if self.translation_errors:
            assert False, "The following modules failed STIX translation {}".format(self.translation_errors) 