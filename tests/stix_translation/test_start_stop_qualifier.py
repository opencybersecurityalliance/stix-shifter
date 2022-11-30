from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.module_discovery import modules_list

translation = stix_translation.StixTranslation()
START_STOP_TIMESTAMPS = {
    "start_stop_no_milliseconds": "START t'2022-11-18T15:00:00Z' STOP t'2022-11-20T16:00:00Z'",
    "start_stop_partial_milliseconds": "START t'2022-11-18T15:00:00.1Z' STOP t'2022-11-20T16:00:00.2Z'",
    "start_stop_full_milliseconds": "START t'2022-11-18T15:00:00.100Z' STOP t'2022-11-20T16:00:00.200Z'"
}
STIX_PATTERN = "[ipv4-addr:value = '192.168.0.100']"


class TestQualifierTimestamps(object):

    def _validate_stix_result(self, result, module, timestamp):
        if 'error' in result:
            if "timestamp" not in result["error"]:
                next
            else:
                assert False, "{} failed to translate timestamp: {}".format(module, timestamp)

    def test_qaulifier_timestamps(self):
        modules = modules_list()
        for module in modules:
            for key, timestamp in START_STOP_TIMESTAMPS.items():
                result = translation.translate(module, 'query', '', STIX_PATTERN + " " + timestamp)
                self._validate_stix_result(result, module, timestamp)