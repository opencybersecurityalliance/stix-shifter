from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
import logging
from os import path
import json
from . import query_constructor

logger = logging.getLogger(__name__)


class QueryTranslator(BaseQueryTranslator):
    def __init__(self, options, dialect, basepath):
        super().__init__(options, dialect, basepath)
        assert len(self.map_data) == 2
        assert "process" in self.map_data and "binary" in self.map_data

    def fetch_mapping(self, not_used_path):
        process_mapping = self._fetch_mapping_file("process_from_stix_map.json")
        binary_mapping = self._fetch_mapping_file("binary_from_stix_map.json")
        return {"binary": binary_mapping, "process": process_mapping}

    def _fetch_mapping_file(self, filename):
        filepath = path.abspath(path.join(self.basepath, "json", filename))
        map_file = open(filepath).read()
        map_data = json.loads(map_file)
        return map_data

    def map_field(self, stix_object_name, stix_property_name):
        results = []
        for dialect in ["binary", "process"]:  # binary api fields mappings are preferred
            mapping = self.map_data[dialect]
            if stix_object_name in mapping and stix_property_name in mapping[stix_object_name]["fields"]:
                results.append((mapping[stix_object_name]["fields"][stix_property_name], dialect))

        if len(results) != 0:
            return results
        else:
            return []

    def transform_query(self, data, antlr_parsing_object):
        """
        Transforms STIX pattern into a different query format. Based on a mapping file
        :param antlr_parsing_object: Antlr parsing objects for the STIX pattern
        :type antlr_parsing_object: object
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into another format. This should default to something if one isn't passed in
        :type mapping: str (filepath)
        :return: transformed query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to cbquery")

        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, self.options)
        return query_string
