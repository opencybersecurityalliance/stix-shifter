from stix_shifter_utils.modules.base.stix_translation.base_query_translator import BaseQueryTranslator
from stix_shifter_utils.stix_translation.src.utils.exceptions import DataMappingException
import logging
from os import path
from stix_shifter_utils.utils.file_helper import read_json

logger = logging.getLogger(__name__)


class CimBaseQueryTranslator(BaseQueryTranslator):

    def __init__(self, options={}, dialect=None):
        super().__init__(options, dialect, path.dirname(__file__))
        self.select_fields = read_json('cim_select_fields', options)
    # TODO:
    # This mapping is not super straightforward. It could use the following improvements:
    # * Registry keys need to pull the path apart from the key name, I believe. Need to investigate with Splunk
    # * Need to validate that the src and dest aliases are working
    # * Need to add in the static attributes, like the `object_category` field
    # * Need to verify "software" == "inventory"
    # * Need to figure out network traffic when it's for web URLs
    # * Hashes are kind of hacky, just hardcoded. Probably needs to be a regex

    def map_object(self, stix_object_name):
        if stix_object_name in self.map_data and self.map_data[stix_object_name] != None:
            return self.map_data[stix_object_name]["cim_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CIM".format(stix_object_name))
