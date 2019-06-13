from stix_shifter.stix_translation.src.utils.exceptions import DataMappingException
from stix_shifter.stix_translation.src.modules.base.base_data_mapper import BaseDataMapper
from os import path


class CimDataMapper(BaseDataMapper):

    FIELDS = {
        "default": [
            "src_ip",
            "src_port",
            "src_mac",
            "src_ipv6",
            "dest_ip",
            "dest_port",
            "dest_mac",
            "dest_ipv6",
            "file_hash",
            "user",
            "url",
            "protocol"
        ]
    }

    def __init__(self, options={}):
        self.options = options
        if 'select_fields' in options:
            self.FIELDS = options['select_fields']
        mapping_json = options.get('mapping')
        basepath = path.dirname(__file__)
        self.MAPPINGS = mapping_json or self.fetch_mapping(basepath)

    # TODO:
    # This mapping is not super straightforward. It could use the following improvements:
    # * Registry keys need to pull the path apart from the key name, I believe. Need to investigate with Splunk
    # * Need to validate that the src and dest aliases are working
    # * Need to add in the static attributes, like the `object_category` field
    # * Need to verify "software" == "inventory"
    # * Need to figure out network traffic when it's for web URLs
    # * Hashes are kind of hacky, just hardcoded. Probably needs to be a regex
    def map_object(self, stix_object_name):
        if stix_object_name in self.MAPPINGS and self.MAPPINGS[stix_object_name] != None:
            return self.MAPPINGS[stix_object_name]["cim_type"]
        else:
            raise DataMappingException("Unable to map object `{}` into CIM".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.MAPPINGS and stix_property_name in self.MAPPINGS[stix_object_name]["fields"]:
            return self.MAPPINGS[stix_object_name]["fields"][stix_property_name]
        else:
            return []


mapper_class = CimDataMapper
