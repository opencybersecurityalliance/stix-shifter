import logging
import importlib

from ...patterns.parser import generate_query
from ..base.base_query_translator import BaseQueryTranslator
from . import splunk_query_constructor

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
DEFAULT_SEARCH_KEYWORD = "search"
DEFAULT_FIELDS = "src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol"

class StixToSplunk(BaseQueryTranslator):

    def transform_query(self, data, options, mapping=None):
        """
        Transforms STIX query into splunk query format. Based on a mapping file
        :param data: STIX query string to transform into splunk query format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to transform the given STIX query into splunk format. This defaults to the from_stix_map.json in the stix_shifter/stix_translation/src/modules/qradar/json/ directory
        :type mapping: str (filepath)
        :return: splunk query string
        :rtype: str
        """

        logger.info("Converting STIX2 Pattern to Splunk query")

        query_object = generate_query(data)
        data_mapper = options.get('data_mapper')
        mapping = options.get('mapping')

        if not data_mapper:
            data_mapper = 'cim'

        data_mapper_module_name = ''.join(["stix_shifter.stix_translation.src.modules.", data_mapper, ".", data_mapper, "_data_mapping"])

        try:
            data_mapper_module = importlib.import_module(data_mapper_module_name)
            data_model_mapper = data_mapper_module.mapper_class(mapping)
        except ModuleNotFoundError:
            raise NotImplementedError(f"Module {data_mapper_module_name} not implemented")
        except AttributeError:
            raise NotImplementedError(f"Module {data_mapper_module_name} does not implement mapper_class attribute")

        result_limit = options['result_limit'] if 'result_limit' in options else DEFAULT_LIMIT
        timerange = options['timerange'] if 'timerange' in options else DEFAULT_TIMERANGE

        # append '-' as prefix and 'minutes' as suffix in timerange to convert minutes in SPL query format
        timerange = '-' + str(timerange) + 'minutes'

        query_string = splunk_query_constructor.translate_pattern(
            query_object, data_model_mapper, result_limit, DEFAULT_SEARCH_KEYWORD, timerange)
        return query_string
