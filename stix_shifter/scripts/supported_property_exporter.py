import json
from os import path

current_dir = path.abspath(path.dirname(__file__))

TRANSLATION_MODULE_PATH = path.abspath(path.join(current_dir, "../../stix_shifter_modules"))
ADAPTER_GUIDE_PATH = path.abspath(path.join(current_dir, '../../adapter-guide'))

# Add new connectors to this dictionary as they become available. The key must match the name of the translation module.
CONNECTORS = {
    "qradar": "QRadar", 
    "splunk": "Splunk Enterprise Security", 
    "bigfix": "BigFix", 
    "carbonblack": "Carbon Black CB Response", 
    "elastic_ecs": "Elasticsearch ECS", 
    "msatp": "Microsoft Defender Advanced Threat Protection",
    "security_advisor": "IBM Cloud Security Advisor",
    "guardium": "IBM Security Guardium",
    "aws_cloud_watch_logs": "Amazon CloudWatch Logs",
    "azure_sentinel": "Microsoft Azure Sentinel"
}


def __main__():

    table_of_contents = "# Currently supported STIX objects and properties\n"
    table_of_contents += "Each connector supports a set of STIX objects and properties as defined in the connector's mapping files. There is also a set of common STIX properties that all cyber observable objects must contain. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for more information on STIX objects.\n"
    table_of_contents += "## Common cyber observable properties\n"
    table_of_contents += "- created\n"
    table_of_contents += "- modified\n"
    table_of_contents += "- first_observed\n"
    table_of_contents += "- last_observed\n"
    table_of_contents += "- number_observed\n\n"
    table_of_contents += "## Supported data sources\n"
    table_of_contents += "Stix-shifter currently offers connector support for the following cybersecurity products. Click on a data source to see a list of STIX attributes and properties it supports.\n\n"

    table_of_contents_file_path = path.abspath(path.join(ADAPTER_GUIDE_PATH, "supported-mappings.md"))
    table_of_contents_file = open(table_of_contents_file_path, "w")

    for index, (key, module) in enumerate(CONNECTORS.items()):
        try:
            filepath = path.abspath(path.join(TRANSLATION_MODULE_PATH, key, "stix_translation/json", "to_stix_map.json"))    
            json_file = open(filepath)
            loaded_json = json.loads(json_file.read())
        except(Exception):
            print("Error for {} module with: {}".format(key))
            continue
        
        stix_attribute_collection = _parse_attributes(loaded_json, key, {})
        json_file.close()
        supported_stix_file_path = path.abspath(path.join(ADAPTER_GUIDE_PATH, "connectors", "{}_supported_stix.md".format(key)))
        supported_stix_file = open(supported_stix_file_path, "w")
        
        output_string = ""
        output_string += "## " + module + "\n"
        table_of_contents += "- [{}]({})\n".format(module, "connectors/{}_supported_stix.md".format(key))
        sorted_objects = json.dumps(stix_attribute_collection, sort_keys=True)
        sorted_objects = json.loads(sorted_objects)
        for stix_object, property_list in sorted_objects.items():
            output_string += "### " + stix_object + "\n"
            for index, prop in enumerate(property_list):
                output_string += "- {}\n".format(prop)
            output_string += "\n___\n"

        supported_stix_file.write(output_string)
        supported_stix_file.close()
    table_of_contents_file.write(table_of_contents)
    table_of_contents_file.close()


def _parse_attributes(element, module, stix_attribute_collection):
    if isinstance(element, list):
        for value in element:
            _parse_attributes(value, module, stix_attribute_collection)
    if isinstance(element, dict) and not element.get("key"):
        for key, value in element.items():
            _parse_attributes(value, module, stix_attribute_collection)
    if isinstance(element, dict) and element.get("key"):
        split_stix_object = element["key"].split(".")
        if len(split_stix_object) == 1:
            return None
        if len(split_stix_object) == 2:
            stix_object = split_stix_object[0]
            stix_property = split_stix_object[1]
        elif len(split_stix_object) == 3:
            stix_object = split_stix_object[0]
            stix_property = split_stix_object[1] + "." + split_stix_object[2]
        stix_object_properties = stix_attribute_collection.get(stix_object)
        if stix_object_properties and stix_property not in stix_object_properties:
            stix_attribute_collection[stix_object].append(stix_property)
        elif not stix_object_properties:
            stix_attribute_collection[stix_object] = [stix_property]
    return stix_attribute_collection



if __name__ == "__main__":
    __main__()
