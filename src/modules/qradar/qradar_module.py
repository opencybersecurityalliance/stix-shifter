#!/usr/bin/env python3
import json
from ..qradar import qradar_translator
from ...base_module import TranslationInterface


class Translator(TranslationInterface):

    def stix_to_datasource_query(self, data, mapping=None):
        # if translating STIX pattern to AQL...
        stix_pattern = data
        translator = qradar_translator.QRadarTranslator()
        aql_query = translator.stix_to_aql(stix_pattern)
        return aql_query

    def datasource_results_to_stix(self, data, mapping=None):
        # if translating QRadar events to STIX...
        translator = qradar_translator.QRadarTranslator()

        json_data = json.loads(data)

        stix_observables = translator.qradar_to_stix(json_data, mapping)

        print(stix_observables)
        return stix_observables
