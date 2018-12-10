import logging
import importlib

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import elastic_query_constructor

logger = logging.getLogger(__name__)


class StixToElastic(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into elastic query format. Based on a mapping file
        :param data: STIX query string to transform into elastic query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into elastic format. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: elastic query string
        :rtype: str
        """

        query_object = generate_query(data)
        data_mapper = options.get('data_mapper')
        if not data_mapper:
            data_mapper = 'car'

        data_mapper_module_name = ''.join(["stix_shifter.stix_translation.src.modules.", data_mapper, ".", data_mapper, "_data_mapping"])

        try:
            data_mapper_module = importlib.import_module(data_mapper_module_name)
            data_model_mapper = data_mapper_module.mapper_class()
        except ModuleNotFoundError:
            raise NotImplementedError(f"Module {data_mapper_module_name} not implemented")
        except AttributeError:
            raise NotImplementedError(f"Module {data_mapper_module_name} does not implement mapper_class attribute")


        query_string = elastic_query_constructor.translate_pattern(
            query_object, data_model_mapper)
        return query_string
