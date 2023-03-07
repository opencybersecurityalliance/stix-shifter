# -*- coding: utf-8 -*-
"""
Converts native results into STIX observability objects.

See: https://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part1-stix-core.html
"""
import json

from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
from stix_shifter_utils.stix_translation.src.utils.exceptions import LoadJsonResultsException, TranslationResultException


class ResultsTranslator(JSONToStix):
    """
    Class that converting native response JSON to SIX observability objects.

    See: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md

    :param options: configuration options, see: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-configuration-json.md
    :type options: object
    :param dialect: dialect of the data set, see: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-stix-adapter.md
    :type dialect: str
    :param base_file_path: base file path to look for STIX mapping specification
    :type base_file_path: str
    """
    def __init__(self, options, dialect, base_file_path=None):
        super().__init__(options, dialect, base_file_path)

    def translate_results(self, data_source, data):
        """
        Translates native data response into STIX object

        :param data_source: dialect specific model mapping data, see: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-translation-module.md#step-2-edit-the-from_stix_map-json-file
        :type data_source: str
        :param data: native data response
        :type data: str
        :return: native query response
        :rtype: STIX object
        """

        try:
            mapped_data = self.map_data
            results = json_to_stix_translator.convert_to_stix(data_source, mapped_data, data, self.transformers, self.options, self.callback)
        except Exception as ex:
            raise TranslationResultException("Error when converting results to STIX: %s" % ex) from ex

        return results
