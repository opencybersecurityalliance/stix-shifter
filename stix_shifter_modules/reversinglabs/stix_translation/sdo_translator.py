from stix_shifter_utils.normalization.BaseNormalization import BaseNormalization
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix_translator import DataSourceObjToStixObj

class SdoTranslator(DataSourceObjToStixObj):
    def create_sighting_sdo(self, sighting_object, indicator_id):
        return DataSourceObjToStixObj.base_normalization.create_sighting_sdo(sighting_object, indicator_id)

    def create_infrastructure_object_sdo(self, infrastructure_object, enriched_ioc, indicator_id):          
        return DataSourceObjToStixObj.base_normalization.create_infrastructure_object_sdo(infrastructure_object, enriched_ioc, indicator_id)  

    def create_malware_sdo(self, malware_object, indicator_id, enriched_ioc):
        return DataSourceObjToStixObj.base_normalization.create_malware_sdo(malware_object, indicator_id, enriched_ioc)

    def create_identity_sdo(self, data_source, namespace):
        return DataSourceObjToStixObj.base_normalization.create_identity_sdo(data_source, namespace)

    def create_extension_sdo(self, identity_object, namespace, nested_properties, toplevel_properties):
        # Create an extension-definition object to be used in conjunction with STIX Indicator object       
        return DataSourceObjToStixObj.base_normalization.create_extension_sdo(identity_object, namespace, nested_properties, toplevel_properties)      

    def create_indicator_sdo(self, indicator_object, identity_id, extension_id, nested_properties, top_properties=None):
        return DataSourceObjToStixObj.base_normalization.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_properties, top_properties)

    def create_stix_bundle(self):
        return DataSourceObjToStixObj.base_normalization.create_stix_bundle()
        
