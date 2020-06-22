from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter_utils.utils import logger
from os import path
import json
from . import query_constructor


class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath, rows=1024):
        super().__init__(options, dialect, basepath)
        self.rows = rows
        self.logger = logger.set_logger(__name__)

    def _fetch_mapping(self, dialect=''):
        try:
            if dialect != '':
                dialect = dialect + '_'
            basepath = path.dirname(__file__)
            filepath = path.abspath(
                path.join(basepath, "json", dialect + "from_stix_map.json"))

            map_file = open(filepath).read()
            map_data = json.loads(map_file)
            return map_data
        except Exception as ex:
            self.logger.error('exception in stix_shifter_modules/csa/stix_translation/query_translator.py::QueryTranslator::_fetch_mapping():' + ex)
            return {}

    def map_object(self, stix_object_name):
        self.map_data = self._fetch_mapping(self.dialect)
        if stix_object_name in self.map_data and self.map_data[stix_object_name] != None:
            return self.map_data[stix_object_name]
        else:
            raise DataMappingException(
                "Unable to map object `{}` into SQL".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        self.map_data = self._fetch_mapping(self.dialect)
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []

    def map_selections(self):
        try:
            filepath = path.abspath(
                path.join(self.basepath, "json", self.dialect + "_event_fields.json"))
            sql_fields_file = open(filepath).read()
            sql_fields_json = json.loads(sql_fields_file)

            # Temporary default selections, this will change based on upcoming config override and the STIX pattern that is getting converted to SQL.
            field_list = sql_fields_json['default']
            sql_select = ", ".join(field_list)
            return sql_select
        except Exception as ex:
            self.logger.error('Exception while reading sql fields file:' + ex)
            return {}

    def transform_query(self, data, antlr_parsing_object):
        """
        Transforms STIX query into sql query format. Based on a mapping file
        :param data: STIX query string to transform into sql query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into sql format. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: sql query string
        :rtype: str
        """

        self.logger.info("Converting STIX2 Pattern to sql")
        query_string = query_constructor.translate_pattern(
            antlr_parsing_object, self, number_rows=self.rows)
        return query_string
