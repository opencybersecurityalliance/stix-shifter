import json
import argparse
from os import path
import re
from datetime import datetime

## Script for generating a table of mappings for each connector based on the operator, from-stix, and to-stix mapping files
## Add --sdo SDO argument for connectors that use SDO mappings instead of a to-stix SCO mapping file
## python supported_property_exporter.py --sdo SDO

current_dir = path.abspath(path.dirname(__file__))

CONNECTOR_MODULE_PATH = path.abspath(path.join(current_dir, "../../stix_shifter_modules"))
ADAPTER_GUIDE_PATH = path.abspath(path.join(current_dir, '../../adapter-guide'))

# Add new connectors to this dictionary as they become available. The key must match the name of the translation module.
# Comment out any connectors you wish to ommit.
SCO_CONNECTORS = {
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
    # "azure_sentinel": "Microsoft Graph Security",
    "alertflex": "Alertflex",
    "arcsight": "Micro Focus ArcSight",
    "aws_athena": "Amazon Athena",
    "crowdstrike": 'CrowdStrike Falcon',
    "trendmicro_vision_one": "Trend Micro Vision One",
    "onelogin": "OneLogin",
    "secretserver": "IBM Security Verify Privilege Vault",
    "sumologic": "Sumo Logic",
    "datadog": "Datadog",
    "proofpoint": "Proofpoint (SIEM API)",
    # "infoblox": "Infoblox BloxOne Threat Defense",
    "cybereason": "Cybereason",
    "paloalto": "PaloAlto Cortex XDR",
    "sentinelone": "SentinelOne",
    "reaqta": "IBM Security QRadar EDR",
    "darktrace": "Darktrace",
    "rhacs": "Red Hat Advanced Cluster Security for Kubernetes (StackRox)",
    "ibm_security_verify": "IBM Security Verify",
    "gcp_chronicle": "GCP Chronicle",
    "azure_log_analytics": "Azure Log Analytics",
    "okta": "Okta"
}

SDO_CONNECTORS = {
    "abuseipdb": "AbuseIPDB",
    "alienvault_otx": "AlienVault OTX",
    "dshield": "SANS ISC DShield",
    "intezer": "Intezer",
    "recorded_future": "Recorded Future",
    "reversinglabs": "ReversingLabs",
    "threat_grid": "Cisco Threat Grid",
    "threat_q": "ThreatQ",
    "virus_total": "VirusTotal"
}

DEFAULT_DIALECT = "default"

DIALECTS = {
    "qradar": ["events", "flows"],
    "aws_athena": ["guardduty", "ocsf", "vpcflow"],
    "aws_cloud_watch_logs": ["guardduty", "vpcflow"],
    "datadog": ["events", "processes"],
    "guardium": ["qsearch", "report"],
    "infoblox": ["dnsEventData", "dossierData", "tideDbData"],
    "paloalto": ["xdr_data"],
    "secretserver": ["event"],
    "trendmicro_vision_one": ["endpointActivityData", "messageActivityData"],
    "azure_log_analytics": ["SecurityAlert", "SecurityEvent", "SecurityIncident"],
    "elastic_ecs": [DEFAULT_DIALECT, "beats"]
}

STIX_OPERATORS = {
    "ComparisonExpressionOperators.And": "AND (Comparision)",
    "ComparisonExpressionOperators.Or": "OR (Comparision)",
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
    "ObservationOperators.Or": "OR (Observation)",
    "ObservationOperators.And": "AND (Observation)",
    "ObservationOperators.FollowedBy": "FOLLOWEDBY"
}

now = datetime.now()
UPDATED_AT = now.strftime("%D")

def __main__():

    # process arguments
    parent_parser = argparse.ArgumentParser(description='mapping_table_generator')
    parent_parser.add_argument('--sdo',help='Generate tables for connectors that use SDO mapping')

    args = parent_parser.parse_args()

    if args.sdo:
        CONNECTORS = SDO_CONNECTORS
    else:
        CONNECTORS = SCO_CONNECTORS

    table_of_contents = "# Currently supported STIX objects and properties\n\n"
    table_of_contents += "Each connector supports a set of STIX objects and properties as defined in the connector's mapping files. There is also a set of common STIX properties that all cyber observable objects must contain. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for more information on STIX objects.\n"
    table_of_contents += "## Common cyber observable properties\n\n"
    table_of_contents += "- created\n"
    table_of_contents += "- modified\n"
    table_of_contents += "- first_observed\n"
    table_of_contents += "- last_observed\n"
    table_of_contents += "- number_observed\n\n"
    table_of_contents += "## Supported data sources\n\n"
    table_of_contents += "Stix-shifter currently offers connector support for the following cybersecurity products. Click on a data source to see a list of STIX attributes and properties it supports.\n\n"

    table_of_contents_file_path = path.abspath(path.join(ADAPTER_GUIDE_PATH, "supported-mappings.md"))
    table_of_contents_file = open(table_of_contents_file_path, "w")

    for _, (key, module) in enumerate(CONNECTORS.items()):

        data_field_alias_mapping = []
        if key == 'qradar':
            try:
                fields_filepath = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "stix_translation/json", "aql_events_fields.json"))    
                fields_json_file = open(fields_filepath)
                loaded_fields_json = json.loads(fields_json_file.read())
                data_field_alias_mapping = loaded_fields_json.get('default') # array of fields
                fields_json_file.close()
            except(Exception):
                print("Error for {} module".format(key))
                continue

        output_string = ""
        output_string += "##### Updated on " + UPDATED_AT + "\n"
        output_string += "## " + module + "\n"
        table_of_contents += "- [{}]({})\n".format(module, "../stix_shifter_modules/{}/{}_supported_stix.md".format(key, key))

        # SDOs
        try:
           output_string = _generate_sdo_list(output_string, args)
        except Exception as e:
            print("Error constructing SDO list for {} module: {}".format(key, e))
            continue

        # OPERATORS
        try:
            filepath = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "stix_translation/json", "operators.json")) 
            operators_json_file = open(filepath)   
            output_string = _generate_operators_table(operators_json_file, output_string)
            operators_json_file.close()
        except Exception as e:
            print("Error constructing STIX operator mapping table for {} module: {}".format(key, e))
            continue

        # FROM-STIX
        try:
            # TODO: Dynamically fetch dialects and wrap in loop to capture all dialects
            dialects = [DEFAULT_DIALECT]
            if key in DIALECTS:
                dialects = DIALECTS[key]
            for dialect in dialects:
                if dialect == DEFAULT_DIALECT:
                    dialect = ""
                    output_string += "### Searchable STIX objects and properties\n"
                    filepath = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "stix_translation/json", "from_stix_map.json"))    
                else:
                    output_string += "### Searchable STIX objects and properties for {} dialect\n".format(dialect.capitalize())
                    filepath = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "stix_translation/json", "{}from_stix_map.json".format(dialect + "_")))    
                from_stix_json_file = open(filepath)
                output_string = _generate_from_stix_table(from_stix_json_file, key, data_field_alias_mapping, output_string)
                from_stix_json_file.close()
        except Exception as e:
            print("Error constructing from-STIX mapping table for {} module: {}".format(key, e))
            continue
        
        # TO-STIX 
        if not args.sdo:
            try:
                filepath = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "stix_translation/json", "to_stix_map.json"))    
                to_stix_json_file = open(filepath) 
                output_string = _generate_to_stix_table(key, to_stix_json_file, data_field_alias_mapping, output_string)
                to_stix_json_file.close()
            except Exception as e:
                print("Error constructing to-STIX mapping table for {} module: {}".format(key, e))
                continue

        try:
            supported_stix_file_path = path.abspath(path.join(CONNECTOR_MODULE_PATH, key, "{}_supported_stix.md".format(key)))
            supported_stix_file = open(supported_stix_file_path, "w")   
            supported_stix_file.write(output_string)
            supported_stix_file.close()
        except Exception as e:
                print("Error writing mapping tables for {} module: {}".format(key, e))
                continue
        
    table_of_contents_file.write(table_of_contents)
    table_of_contents_file.close()

def _generate_sdo_list(output_string, args):
    output_string += "### Results STIX Domain Objects\n"
    if args.sdo:
        output_string += "* Identity\n* Sighting\n* Infrastructure\n* Malware\n* Extension\n* Indicator\n"
    else:
        output_string += "* Identity\n* Observed Data\n"
    output_string += "<br>\n"
    return output_string

def _generate_operators_table(operators_json_file, output_string):
    loaded_operators_json = json.loads(operators_json_file.read())
    stix_operator_collection = _parse_operators(loaded_operators_json, {})
    output_string += "### Supported STIX Operators\n"
    output_string += "*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*\n\n"
    output_string += "| STIX Operator | Data Source Operator |\n"
    output_string += "|--|--|\n"
    for stix_operator, ds_operator in stix_operator_collection.items():
        output_string += "| {} | {} |\n".format(stix_operator, ds_operator)
    output_string += "| <br> | |\n"
    return output_string

def _generate_from_stix_table(from_stix_json_file, key, data_field_alias_mapping, output_string):
    loaded_from_stix_json = json.loads(from_stix_json_file.read())
    if key == 'cybereason':
        output_string += "*The Cybereason connector can only join specific linked fields with the AND operator as defined in its [configmap](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/aws_athena/stix_translation/json/operators.json).*\n\n"
    output_string += "| STIX Object and Property | Mapped Data Source Fields |\n"
    output_string += "|--|--|\n"
    for stix_object_key, value in loaded_from_stix_json.items():
        property_dictionary = value["fields"]
        for s_property, fields_list in property_dictionary.items():
            if not isinstance(fields_list, list):
                fields_list = [fields_list]
            orig_fields_list = []
            if data_field_alias_mapping:
                # TODO: Get real field name for QRadar
                for aliased_field in fields_list:
                    orig_data_field = _get_data_field(aliased_field, data_field_alias_mapping)
                    orig_fields_list.append(orig_data_field)
            else:
                orig_fields_list = fields_list
            output_string += "| **{}**:{} | {} |\n".format(stix_object_key, s_property, ', '.join(map(str, orig_fields_list)))
    output_string += "| <br> | |\n"
    return output_string

def _generate_to_stix_table(key, to_stix_json_file, data_field_alias_mapping, output_string):
    loaded_to_stix_json = json.loads(to_stix_json_file.read())
    stix_attribute_collection = _parse_attributes(loaded_to_stix_json, key, {})
    sorted_attribute_objects = json.dumps(stix_attribute_collection, sort_keys=True)
    sorted_attribute_objects = json.loads(sorted_attribute_objects)
    output_string += "### Supported STIX Objects and Properties for Query Results\n"
    output_string += "| STIX Object | STIX Property | Data Source Field |\n"
    output_string += "|--|--|--|\n"
    for stix_object, property_list in sorted_attribute_objects.items():
        for index, prop in enumerate(property_list):
            stix_property, data_field = prop.split(":")
            if data_field_alias_mapping:
                data_field = _get_data_field(data_field, data_field_alias_mapping)
            output_string += "| {} | {} | {} |\n".format(stix_object, stix_property, data_field)
        output_string += "| <br> | | |\n"
    return output_string


def _get_data_field(data_field, data_field_alias_mapping):
    for value in data_field_alias_mapping:
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
