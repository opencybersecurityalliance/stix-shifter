from stix_shifter_utils.normalization.BaseNormalization import BaseNormalization

class SdoTranslator(BaseNormalization):
    def create_sighting_sdo(self, sighting_object, indicator_id):
        return super().create_sighting_sdo(sighting_object, indicator_id)    

    def create_infrastructure_object_sdo(self, infrastructure_object, enriched_ioc, indicator_id):          
        return super().create_infrastructure_object_sdo(infrastructure_object, enriched_ioc, indicator_id)  

    def create_malware_sdo(self, malware_object, indicator_id, enriched_ioc):
        return super().create_malware_sdo(malware_object, indicator_id, enriched_ioc)

    def create_identity_sdo(self, data_source, namespace):
        return super().create_identity_sdo(data_source, namespace)

    def create_extension_sdo(self, identity_object, namespace, nested_properties, toplevel_properties):
        # Create an extension-definition object to be used in conjunction with STIX Indicator object       
        return super().create_extension_sdo(identity_object, namespace, nested_properties, toplevel_properties)      

    def create_indicator_sdo(self, indicator_object, identity_id, extension_id, nested_properties, top_properties=None):
        return super().create_indicator_sdo(indicator_object, identity_id, extension_id, nested_properties, top_properties)
