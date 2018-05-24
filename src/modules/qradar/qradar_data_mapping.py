class QRadarDataMapper:

    MAPPINGS = {
        "ipv4-addr": {
            "fields": {
                "value": "destinationip"
            }
        }
    }

    def map_object(self, stix_object_name):
        if stix_object_name in self.MAPPINGS and self.MAPPINGS[stix_object_name] != None:
            return self.MAPPINGS[stix_object_name]
        else:
            raise DataMappingException(
                "Unable to map object `{}` into AQL".format(stix_object_name))

    def map_field(self, stix_object_name, stix_property_name):
        if stix_object_name in self.MAPPINGS and stix_property_name in self.MAPPINGS[stix_object_name]["fields"]:
            return self.MAPPINGS[stix_object_name]["fields"][stix_property_name]
        else:
            raise DataMappingException("Unable to map property `{}:{}` into AQL".format(
                stix_object_name, stix_property_name))
