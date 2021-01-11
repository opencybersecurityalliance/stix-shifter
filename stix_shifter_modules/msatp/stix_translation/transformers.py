from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer


class MsatpToTimestamp(ValueTransformer):
    """A value transformer to truncate milliseconds"""

    @staticmethod
    def transform(msatptime):
        time_array = msatptime.split('.')
        converted_time = time_array[0] + '.' + time_array[1][:3] + 'Z' if len(time_array) > 1 else time_array[0] + 'Z'
        return converted_time



class MsatpToRegistryValue(ValueTransformer):
    """A value transformer to convert MSATP Registry value protocol to windows-registry-value-type STIX"""

    @staticmethod
    def transform(registryvalues):
        stix_mapping = {"RegistryValueName": "name", "RegistryValueData": "data", "RegistryValueType": "data_type"}
        stix_datatype_mapping = {"None": "REG_NONE", "String": "REG_SZ", "Dword": "REG_DWORD",
                                 "ExpandString": "REG_EXPAND_SZ", "MultiString": "REG_MULTI_SZ",
                                 "Binary": "REG_BINARY", "Qword": "REG_QWORD"}
        converted_value = list()
        registryvalue_dict = dict()
        for each_value in registryvalues:
            for key, value in each_value.items():
                is_data_add = True
                if key == "RegistryValueType":
                    if value in stix_datatype_mapping.keys():
                        value = stix_datatype_mapping[value]
                    else:
                        is_data_add = False
                if is_data_add:
                    registryvalue_dict.update({stix_mapping[key]: value})
        converted_value.append(registryvalue_dict)
        return converted_value

