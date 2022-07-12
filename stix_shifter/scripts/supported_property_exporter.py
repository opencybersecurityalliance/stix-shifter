import json
from os import path
import re
from datetime import datetime

current_dir = path.abspath(path.dirname(__file__))

TRANSLATION_MODULE_PATH = path.abspath(path.join(current_dir, "../../stix_shifter_modules"))
ADAPTER_GUIDE_PATH = path.abspath(path.join(current_dir, '../../adapter-guide'))

# Add new connectors to this dictionary as they become available. The key must match the name of the translation module.
CONNECTORS = {
    "qradar": "IBM QRadar", 
    "splunk": "Splunk Enterprise Security", 
    "bigfix": "HCL BigFix", 
    "carbonblack": "Carbon Black CB Response",
    "cbcloud": "Carbon Black Cloud", 
    "elastic_ecs": "Elasticsearch ECS", 
    "msatp": "Microsoft Defender for Endpoint",
    # "security_advisor": "IBM Cloud Security Advisor",
    "guardium": "IBM Guardium Data Protection",
    "aws_cloud_watch_logs": "Amazon CloudWatch Logs",
    "azure_sentinel": "Microsoft Azure Sentinel",
    "alertflex": "Alertflex",
    "arcsight": "Micro Focus ArcSight",
    "aws_athena": "Amazon Athena",
    "crowdstrike": 'CrowdStrike Falcon',
    "trendmicro_vision_one": "Trend Micro Vision One",
    "onelogin": "OneLogin",
    "secretserver": "Secret Server",
    "sumologic": "Sumo Logic",
    "datadog": "Datadog",
    "proofpoint": "Proofpoint (SIEM API)",
    # "infoblox": "Infoblox BloxOne Threat Defense",
    "cybereason": "Cybereason",
    "paloalto": "PaloAlto Cortex XDR",
    "sentinelone": "SentinelOne",
    "reaqta": "ReaQta",
    "darktrace": "Darktrace"
}

STIX_OPERATORS ={
    "ComparisonExpressionOperators.And": "AND",
    "ComparisonExpressionOperators.Or": "OR",
    "ComparisonComparators.GreaterThan": ">",
    "ComparisonComparators.GreaterThanOrEqual": ">=",
    "ComparisonComparators.LessThan": "<",
    "ComparisonComparators.LessThanOrEqual": "<=",
    "ComparisonComparators.Equal": "=",
    "ComparisonComparators.NotEqual": "!=",
    "ComparisonComparators.Like": "LIKE",
    "ComparisonComparators.In": "IN",
    "ComparisonComparators.Matches": "MATCHES",
    "ComparisonComparators.IsSubSet": "ISSUBSET",
    "ComparisonComparators.IsSuperSet": "ISSUPERSET",
    "ComparisonComparators.Exists": "EXISTS",
    "ObservationOperators.Or": "OR",
    "ObservationOperators.And": "AND",
    "ObservationOperators.FollowedBy": "FOLLOWEDBY"
}

now = datetime.now()
UPDATED_AT = now.strftime("%D")

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
            to_stix_json_file = open(filepath)
            loaded_to_stix_json = json.loads(to_stix_json_file.read())
            filepath = path.abspath(path.join(TRANSLATION_MODULE_PATH, key, "stix_translation/json", "operators.json")) 
            operators_json_file = open(filepath)   
            loaded_operators_json = json.loads(operators_json_file.read())

        except(Exception):
            print("Error for {} module".format(key))
            continue

        aliased_data_fields = []
        if key == 'qradar':
            try:
                fields_filepath = path.abspath(path.join(TRANSLATION_MODULE_PATH, key, "stix_translation/json", "aql_events_fields.json"))    
                fields_json_file = open(fields_filepath)
                loaded_fields_json = json.loads(fields_json_file.read())
                aliased_data_fields = loaded_fields_json.get('default') # array of fields
                fields_json_file.close()
            except(Exception):
                print("Error for {} module".format(key))
                continue
        
        stix_attribute_collection = _parse_attributes(loaded_to_stix_json, key, {})
        stix_operator_collection = _parse_operators(loaded_operators_json, {})
        supported_stix_file_path = path.abspath(path.join(ADAPTER_GUIDE_PATH, "connectors", "{}_supported_stix.md".format(key)))
        supported_stix_file = open(supported_stix_file_path, "w")
        
        output_string = ""
        output_string += "##### Updated on " + UPDATED_AT + "\n"
        output_string += "## " + module + "\n"
        table_of_contents += "- [{}]({})\n".format(module, "connectors/{}_supported_stix.md".format(key))
        output_string += "### Supported STIX Operators\n"
        output_string += "| STIX Operator | Data Source Operator |\n"
        output_string += "|--|--|\n"
        for stix_operator, ds_operator in stix_operator_collection.items():
            output_string += "| {} | {} |\n".format(stix_operator, ds_operator)
        output_string += "| <br> | |\n"
        operators_json_file.close()
        sorted_attribute_objects = json.dumps(stix_attribute_collection, sort_keys=True)
        sorted_attribute_objects = json.loads(sorted_attribute_objects)
        output_string += "### Supported STIX Objects and Properties\n"
        output_string += "| STIX Object | STIX Property | Data Source Field |\n"
        output_string += "|--|--|--|\n"
        for stix_object, property_list in sorted_attribute_objects.items():
            for index, prop in enumerate(property_list):
                stix_property, data_field = prop.split(":")
                if aliased_data_fields:
                    data_field = _get_data_field(data_field, aliased_data_fields)
                output_string += "| {} | {} | {} |\n".format(stix_object, stix_property, data_field)
            output_string += "| <br> | | |\n"
        to_stix_json_file.close()
        supported_stix_file.write(output_string)
        supported_stix_file.close()
    table_of_contents_file.write(table_of_contents)
    table_of_contents_file.close()


def _get_data_field(data_field, aliased_data_fields):
    for value in aliased_data_fields:
        pattern_match = re.search("\sas\s{}$".format(data_field), value)
        if pattern_match:
            data_field = re.sub(pattern_match[0], "", value)
            break
    return data_field


def _parse_attributes(element, module, stix_attribute_collection, data_source_field=None):
    if isinstance(element, list):
        for value in element:
            _parse_attributes(value, module, stix_attribute_collection, data_source_field)
    if isinstance(element, dict) and not element.get("key"): # Outer layer of mapping
        for key, value in element.items():
            _parse_attributes(value, module, stix_attribute_collection, key)
    if isinstance(element, dict) and element.get("key"):
        if isinstance(element["key"], dict): # Case where there is a "key" field coming from the data source
            for key, value in element.items():
                _parse_attributes(value, module, stix_attribute_collection, data_source_field)
        else:
            split_stix_object = element["key"].split(".")
            if len(split_stix_object) == 0 or len(split_stix_object) == 1:
                return None
            else:
                stix_object = split_stix_object.pop(0)
                stix_property = ""
                while len(split_stix_object) > 0:
                    stix_property += split_stix_object.pop(0)
                    if len(split_stix_object) > 0:
                        stix_property += "."
                stix_property += ":{}".format(data_source_field)
            stix_object_properties = stix_attribute_collection.get(stix_object)
            if stix_object_properties and stix_property not in stix_object_properties:
                stix_attribute_collection[stix_object].append(stix_property)
            elif not stix_object_properties:
                stix_attribute_collection[stix_object] = [stix_property]
    # print("COLLECTION {}".format(stix_attribute_collection))
    return stix_attribute_collection

def _parse_operators(element, operator_collection):
    for key, value in element.items():
        operator_collection[STIX_OPERATORS[key]] = value
    return operator_collection



if __name__ == "__main__":
    __main__()
