from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
import json
import uuid
from urllib.parse import urlparse
from ipaddress import ip_network, IPv4Network, IPv6Network
# from stix_shifter_utils.normalization.normalization_helper import create_attributes, evaluate_attribute_type


def create_attributes(attribute_fields, data):
  threat_attribute_report = []
  if isinstance(attribute_fields, dict):
    for attribute, value in attribute_fields.items():
      if attribute in data:
        attribute_dict = {}
        attribute_dict['attribute_name'] = value
        attribute_dict['attribute_value'] = str(data[attribute])
        attribute_dict['attribute_type'] = evaluate_attribute_type(data[attribute])
        threat_attribute_report.append(attribute_dict) if attribute_dict['attribute_type'] is not None else ''
  elif type(attribute_fields) is str:
    attribute_dict = {}
    attribute_dict['attribute_name'] = attribute_fields
    attribute_dict['attribute_value'] = str(data)
    attribute_dict['attribute_type'] = evaluate_attribute_type(data)
    threat_attribute_report.append(attribute_dict) if attribute_dict['attribute_type'] is not None else ''
  return threat_attribute_report


def evaluate_attribute_type(attribute):
  # supported types = string, number, uri, ip, lat_lng
  attribute_type = None
  if isinstance(attribute, bool):
    attribute_type = 'string' if attribute is True else None
  elif isinstance(attribute, (int, float, complex)):
    attribute_type = 'number'
  if isinstance(attribute, (str)):
    attribute_type = 'string'
    if uri_validator(attribute):
      attribute_type = 'uri'
    try:
      if isinstance(ip_network(attribute), (IPv4Network, IPv6Network)):
        attribute_type = 'ip'
    except ValueError:
      pass

  return attribute_type


def uri_validator(x):
  result = urlparse(x)
  return all([result.scheme, result.netloc])


class ResultsTranslator(BaseResultTranslator):

  # Get indicator_types value
  def get_indicator_types(self, value):
    if value == 'malicious':
      return 'malicious-activity'
    elif value == 'suspicious':
      return 'anomalous-activity'
    elif value == 'trusted' or value == 'no_threats':
      return 'benign'
    # if key/value pair is not included in the report
    elif value is None:
      return
    else:
      return 'unknown'

  def find_hash_type_by_length(self, value):
    HASH_LENGTH = {'40': 'sha-1', '64': 'sha-256', '32': 'md5'}
    hash_type = HASH_LENGTH.get(str(len(value)), '')
    if hash_type in ['sha-1', 'sha-256']:
        return "file:hashes.'{}'".format(hash_type.upper())
    else:
        return "file:hashes.{}".format(hash_type.upper())

  #Get permalink from the report
  def get_external_reference_from_json(self, data):
    url = data['external_reference']
    external_reference = {"external_references":[url]}
    return external_reference

  #return optional fields for indicators such as name, description, indicator-type, kill-chain-phases etc
  def get_optional_values(self, data):

    value = ''
    for ds_key in data:
      if ds_key == "report":
        if len(data[ds_key]) > 0 and 'verdict' in data[ds_key][0]:
            value = data[ds_key][0]['verdict']
        indicator_types_value = self.get_indicator_types(value)
        indicator_types = {"indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
        return indicator_types
    return {"indicator_types": ['unknown']}

  def get_description(self, data):
    for ds_key in data:
      if ds_key == "report":
        if len(data[ds_key]) > 0 and 'summary' in data[ds_key][0] and 'description' in data[ds_key][0]['summary']:
          description = {"description" : "Report - " + data[ds_key][0]['summary']['description']}
        elif len(data[ds_key]) > 0 and 'verdict' in data[ds_key][0]:
          description = {"description" : "Report - This file is " + data[ds_key][0]['verdict']}
        else:
          description = {"description" : "Report - No information"}
        return description
    return None

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Analyzer result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern

  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "url", "unknown"],
    if pattern_type == "url":
      pattern = "["+ pattern_type + ":value='" + value + "']"
      return pattern

    elif pattern_type == 'domain':
      pattern = "["+ pattern_type + "-name:value='" + value + "']"
      return pattern

    # Get Hash of type SHA-256, SHA-1, or MD5
    elif pattern_type == 'hash':
      pattern_type = self.find_hash_type_by_length(value)
      pattern = "["+ pattern_type + "='" + value + "']"
      return pattern

    return pattern
  
  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object
  
  def malware_from_report_attributes(self,data):
    try:
      malware_objects=[]            
      json_data = data
      dataType = json_data['dataType']

      if 'report' in json_data and dataType == 'hash':
        report = json_data['report']
        if not isinstance(report, list):
          report = [report]
        for full_report in report:
          if 'code_reuse' in full_report and 'families' in  full_report['code_reuse']:
            for families in full_report['code_reuse']['families']:
              if  'family_type' in families and families['family_type'] == 'malware':
                if 'family_name' in families:
                  malwareObject={}
                  malwareObject['malware_types'] = [families.get('family_name')]
                  malwareObject['name'] = families.get('family_name')
                  malwareObject['is_family'] = True
                  if (malwareObject not in malware_objects):
                    malware_objects.append(malwareObject)

      return malware_objects
      
    except ValueError:
      raise ValueError("Exception occured to parse report data for malware SDO")

  def get_threat_score(self, data, indicator):
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    if 'threat_score' in data['report'][0]:
      return {"threat_score": data['report'][0]['threat_score']}

    if indicator['indicator_types'][0] == 'unknown':
      return {"threat_score": UNKNOWN_SCORE_MIN}

    dynamic_ttps = data['report'][0]['dynamic_ttps'] if 'dynamic_ttps' in data['report'][0] else None

    if indicator['indicator_types'][0] == 'benign' and not dynamic_ttps:
      return {"threat_score": BENIGN_SCORE_MIN}

    threat_score = severity = 0
    if dynamic_ttps and isinstance(dynamic_ttps, list) and len(dynamic_ttps) > 0:
      for ttps in dynamic_ttps:
        if 'severity' in ttps:
          severity += ttps['severity']
      threat_score = severity / len(dynamic_ttps)

    range_min = 0
    # range_max is 6 since the severity level ranges from 1-3 so 1+2+3 = 6
    range_max = 6

    if(indicator['indicator_types'][0] == 'benign'):
      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    elif (indicator['indicator_types'][0] == 'anomalous-activity'):
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    else:
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    threat_score = {"threat_score": round(tis_score, 1)}
    
    return threat_score


  def get_threat_report(self, data):
    report = {'x_ibm_original_threat_feed_data': {'full': data['report']}}
    return report


  def get_threat_attributes(self, data):
    threat_attribute_report = []

    if 'report' in data:
      full_report = data['report'][0]
      
      full_fields = {
        'analysis_id': 'Analysis ID',
        'family_id': 'Family ID',
        'family_name': 'Family Name',
        'sub_verdict': 'Sub Verdict',
      }

      code_reuse_fields = { 
        'common_gene_count': 'Common Gene Count',
        'gene_count': 'Gene Count',
        'gene_type': 'Gene Type',
        'unique_gene_count': 'Unique Gene Count'
      }
      
      summary_fields = {
        'description': 'Description',
        'main_connection_gene_count': 'Main Connection Gene Count',
        'main_connection_gene_percentage': 'Main Connection Gene Percentage',
        'title': 'Summary Title',
      }

      field_dict = { 
        'code_reuse': code_reuse_fields,
        'summary': summary_fields
      }


      for attribute_keys, attribute_value in field_dict.items():
        if full_report.get(attribute_keys):
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      for attribute_keys, attribute_value in full_fields.items():
        if full_report.get(attribute_keys):
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def translate_results(self, data_source, data):
    """
    Translates JSON data into STIX results based on a mapping file
    :param data: JSON formatted data to translate into STIX format
    :type data: str
    :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX.
        Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
    :type mapping: str (filepath)
    :return: STIX formatted results
    :rtype: str
    """
    json_data = data[0]
    ANALYZER_NAME = 'Intezer_Connector'
    data_source['id'] = ANALYZER_NAME

    # Add Namespace
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = ANALYZER_NAME

    pattern = self.get_pattern_from_json(json_data)
    if('external_reference' in json_data):
      external_reference = self.get_external_reference_from_json(json_data)
    else:
      external_reference = {}  

    indicator_types = self.get_optional_values(json_data)
    description = self.get_description(json_data)
    threat_score = self.get_threat_score(json_data, indicator_types)
    threat_attributes = self.get_threat_attributes(json_data)
    data_to_enrich_pattern = pattern['pattern']
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)

    # Append to stix map json
    # Convert to function
    if (len(json_data['report']) == 0):

      json_data['report'] = [{'message': 'IOC not found'}]

    # Create STIX Bundle and add SDOs
    sdo_translator_object = sdo_translator.SdoTranslator(self.options)
    stix_bundle = sdo_translator_object.create_stix_bundle()

    # Add Identity SDO
    identity_object = sdo_translator_object.create_identity_sdo(data_source, NAMESPACE)
    stix_bundle['objects'] += identity_object

    # Add extension-definition SDO
    toplevel_properties = ['x_ibm_original_threat_feed_data', 'threat_score']
    nested_properties = []
    if (threat_attributes):
      toplevel_properties.append('threat_attributes')

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attributes):
      top_indicator.append(threat_attributes)

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

    # Add Malware SDO    
    malware_object = self.malware_from_report_attributes(json_data); 
    if malware_object:   
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object,indicator_stix_object[0]['id'], data_to_enrich_pattern)
      stix_bundle['objects'] += malware_stix_object

    return stix_bundle