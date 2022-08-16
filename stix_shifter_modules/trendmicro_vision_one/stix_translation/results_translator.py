# -*- coding: utf-8 -*-

from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.stix_translation.src.utils.exceptions import LoadJsonResultsException, TranslationResultException


class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect, base_file_path=None):
        super().__init__(options, dialect, base_file_path)

    def translate_results(self, data_source, data):
        try:
            if self.dialect == "endpointActivityData":
                for log in data:
                    registry_value = log.get("objectRegistryValue")
                    if registry_value:
                        registry_value_type = {"name": registry_value}
                        registry_data = log.get("objectRegistryData")
                        if registry_data:
                            registry_value_type["data"] = registry_data
                        log["objectRegistryValueType"] = [registry_value_type]
            elif self.dialect == "messageActivityData":
                for log in data:
                    message_id = log.get("mail_message_id")
                    if message_id:
                        headers = log.get("mail_internet_headers")
                        if headers:
                            headers.append({"HeaderName": "Message-ID", "Value": message_id})
                        else:
                            log["mail_internet_headers"] = [{"HeaderName": "Message-ID", "Value": message_id}]
        except Exception as e:
            raise LoadJsonResultsException() from e

        try:
            results = json_to_stix_translator.convert_to_stix(data_source, self.map_data, data, self.transformers, self.options, self.callback)
        except Exception as ex:
            raise TranslationResultException("Error when converting results to STIX: %s" % ex) from ex

        return results
