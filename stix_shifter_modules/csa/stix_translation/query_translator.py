from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.file_helper import read_json
from . import query_constructor


class QueryTranslator(BaseQueryTranslator):

    def __init__(self, options, dialect, basepath, rows=1024):
        super().__init__(options, dialect, basepath)
        self.rows = rows
        self.logger = logger.set_logger(__name__)
        self.map_data = read_json(f"{dialect}_from_stix_map", options)
        self.select_fields = read_json(f"{dialect}_event_fields", options)

    def map_object(self, stix_object_name):
        if stix_object_name in self.map_data and self.map_data[stix_object_name] is not None:
            return self.map_data[stix_object_name]
        else:
            raise DataMappingException(
                "Unable to map object `{}` into SQL".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.map_data and stix_property_name in self.map_data[stix_object_name]["fields"]:
            return self.map_data[stix_object_name]["fields"][stix_property_name]
        else:
            return []

    def map_selections(self):
        # Temporary default selections, this will change based on upcoming config override and the STIX pattern that is getting converted to SQL.
        # ^ is it still relevant?
        field_list = self.select_fields['default']
        sql_select = ", ".join(field_list)
        return sql_select

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
