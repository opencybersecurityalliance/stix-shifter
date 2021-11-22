# -*- coding: utf-8 -*-
import json

from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.stix_translation.src.utils.exceptions import LoadJsonResultsException, TranslationResultException


class ResultsTranslator(JSONToStix):

    def __init__(self, options, dialect, base_file_path=None):
        super().__init__(options, dialect, base_file_path)

    def translate_results(self, data_source, data):
        try:
            json_data = json.loads(data)
            data_source = json.loads(data_source)
        except Exception as exc:
            raise LoadJsonResultsException() from exc

        try:
            mapped_data = self.map_data
            results = json_to_stix_translator.convert_to_stix(data_source, mapped_data, json_data, self.transformers, self.options, self.callback)
        except Exception as ex:
            raise TranslationResultException("Error when converting results to STIX: %s" % ex) from ex

        return results
