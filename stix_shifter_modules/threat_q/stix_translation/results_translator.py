from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
from . import sdo_translator
from os import path
import json
from ipaddress import ip_network, IPv4Network, IPv6Network
from stix_shifter_utils.utils import logger
import uuid
from urllib.parse import urlparse


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
    if value == 'Active':
      return 'malicious-activity'
    elif value == 'Indirect' or value == 'Expired':
      return 'anomalous-activity'
    elif value == 'Whitelisted':
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

  def get_ip_address(self, ip):
    return 'ipv4' if isinstance(ip_network(ip), IPv4Network) else 'ipv6'

  #Get permalink from the report
  def get_external_reference_from_json(self, data):
    ext_data = data['external_reference']
    if ext_data.get('url') == '' or ext_data.get('url') == 'N/A':
      return None
    url = data['external_reference']
    external_reference = {"external_references":[url]}
    return external_reference

  #return optional fields for indicators such as name, description, indicator-type, kill-chain-phases etc
  def get_optional_values(self, data):
    value = 'InActive'
    for ds_key in data:
      if ds_key == "report":
        #print (data[ds_key])
        if len(data[ds_key]) > 0:
          value = data[ds_key][0]['status']['name']
        indicator_types_value = self.get_indicator_types(value)
        indicator_types = {"indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
        return indicator_types
    return {"indicator_types": ['unknown']}

  def get_description(self, data):
    for ds_key in data:
      if ds_key == "report":
        if len(data[ds_key]) > 0:
          description = {"description" : "Report - " + data[ds_key][0]['status']['description'] + " Score: " + str(data[ds_key][0]['score'])}
        else:
          description = {"description" : "Report - No information"}
        return description
    return None

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Connector result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern

  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "ip", "url", "unknown"],
    if pattern_type == "url":
      pattern = "["+ pattern_type + ":value='" + value + "']"
      return pattern

    elif pattern_type == 'domain':
      pattern = "["+ pattern_type + "-name:value='" + value + "']"
      return pattern
  
    # Get ipv4 or ipv6
    elif pattern_type == 'ip':
      pattern_type = self.get_ip_address(value)
      pattern = "["+ pattern_type + "-addr:value='" + value + "']"
      return pattern

    # Get Hash of type SHA-256, SHA-1, or MD5
    elif pattern_type == 'hash':
      pattern_type = self.find_hash_type_by_length(value)
      pattern = "["+ pattern_type + "='" + value + "']"
      return pattern

    return pattern


  def get_threat_score(self, data, indicator):
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    if indicator['indicator_types'][0] == 'unknown':
      return {"threat_score": UNKNOWN_SCORE_MIN}

    threat_score = data['report'][0]['score']

    # Declare constants

    range_min = 0
    range_max = 10

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


  # def infrastructure_from_report_attributes(self,data):
  #   try:   
  #     infra_attributes ={}     
  #     json_data = data[0]
  #     category=[]                         
  #     for sub in json_data['report'][0]['attributes']:
  #       if ('Category' == sub['name']) or ('Subcategory' == sub['name']):        
  #         category.append(sub['value'])           
    
  #     infra_attributes['infrastructure_types'] = category
  #     return infra_attributes
  #   except ValueError:
  #     raise ValueError("Exception occured to parse report data for Infrastructure SDO")


  # def malware_from_report_attributes(self,data):
  #   try:   
  #     malware_attributes ={}     
  #     json_data = data[0]
  #     malware_family=[]
  #     isFamily = "false"
  #     if json_data['data'] != 'hash':
  #       isFamily = "true"
        
  #     for sub in json_data['report'][0]['attributes']:
  #       if 'Malware Family' == sub['name']:          
  #         malware_family.append(sub['value'])        
        
  #     malware_attributes['malware_types'] = malware_family
  #     malware_attributes['is_Family'] = isFamily

  #     return malware_attributes
  #   except ValueError:
  #     raise ValueError("Exception occured to parse report data for malware SDO")


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    report = {'x_ibm_original_threat_feed_data': {'full': data['report']}}
    return report


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    if 'report' in data:
      full_report = data['report'][0] if data['report'] else None
      if not full_report: return None


      status_fields = { 
        'name': 'ThreatQ Status',
        'id': 'ThreatQ Status id',
        'description': 'ThreatQ Status Description'
      }


      threatq_id = full_report.get('id')
      if threatq_id:
        id_dict = {
          'attribute_name': 'ThreatQ ID',
          'attribute_value': threatq_id,
          'attribute_type': evaluate_attribute_type(threatq_id)
        }
        threat_attribute_report.append(id_dict)


      field_dict = { 'status': status_fields, }


      for attribute_keys, attribute_value in field_dict.items():
        if attribute_keys in full_report:
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])


      # Add sources
      sources_report = full_report.get('sources')
      if sources_report:
        threat_attribute_report.extend(self.get_sources_attributes(sources_report))

      # Add adversaries
      adversaries_report = full_report.get('adversaries')
      if adversaries_report:
        threat_attribute_report.extend(self.get_adversaries_attributes(adversaries_report))

      # Add attributes
      attribute_report = full_report.get('enrich_info', {}).get('attributes')
      if attribute_report:
        threat_attribute_report.extend(self.get_attribute_attributes(attribute_report))

      # Add malware
      malware_report = full_report.get('relationships', {}).get('malware')
      if malware_report:
        threat_attribute_report.extend(self.get_pattern_attributes(malware_report, 'Malwares'))

      # Add attack_pattern
      attack_pattern_report = full_report.get('relationships', {}).get('attack_pattern')
      if attack_pattern_report:
        threat_attribute_report.extend(self.get_pattern_attributes(attack_pattern_report, 'Attack Patterns'))

      # Add campaign
      campaign_report = full_report.get('relationships', {}).get('campaign')
      if campaign_report:
        threat_attribute_report.extend(self.get_pattern_attributes(campaign_report, 'Attack Campaigns'))

      # Add ttp
      ttp_report = full_report.get('relationships', {}).get('ttp')
      if ttp_report:
        threat_attribute_report.extend(self.get_pattern_attributes(ttp_report, 'Attack TTPs'))

      # Add tool
      tool_report = full_report.get('relationships', {}).get('tool')
      if tool_report:
        threat_attribute_report.extend(self.get_pattern_attributes(tool_report, 'Attack Tools'))


    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def get_sources_attributes(self, sources_list: list) -> list:
    threat_attribute_report = []
    value = ''
    for source in sources_list:
      value += source['name'] + ', '
    if value:
      value = value[:-2]
    attribute_name = 'ThreatQ Sources'
    sources_dict = {
      'attribute_name': attribute_name,
      'attribute_value': value,
      'attribute_type': evaluate_attribute_type(value)
    }
    threat_attribute_report.append(sources_dict)
    return threat_attribute_report


  def get_attribute_attributes(self, attribute_report):
    threat_attribute_report = []
    for attributes in attribute_report:
      attribute_dict = {
        'attribute_name': attributes['name'],
        'attribute_value': attributes['value'],
        'attribute_type': evaluate_attribute_type(attributes['value'])
      }
      for sources in  attributes['sources']:
        attribute_dict['attribute_source'] = sources['name']
        attribute_dict['attribute_updated_at'] = sources['updated_at']
        threat_attribute_report.append(attribute_dict)
    return threat_attribute_report


  def get_pattern_attributes(self, pattern_list: list, attribute_pattern_name: str) -> list:
    threat_attribute_report = []
    value = ''
    for pattern in pattern_list:
      value += pattern['value'] + ', '
    if value:
      value = value[:-2]
    attribute_name = 'Related {}'.format(attribute_pattern_name)
    attack_dict = {
      'attribute_name': attribute_name,
      'attribute_value': value,
      'attribute_type': evaluate_attribute_type(value)
    }
    threat_attribute_report.append(attack_dict)
    return threat_attribute_report


  def get_adversaries_attributes(self, adversaries_list: list) -> list:
      threat_attribute_report = []
      value = ''
      for adversary in adversaries_list:
        value += adversary['name'] + ', '
      if value:
        value = value[:-2]
        attribute_name = 'Related Adversaries'
        adversaries_dict = {
          'attribute_name': attribute_name,
          'attribute_value': value,
          'attribute_type': evaluate_attribute_type(value)
        }
        threat_attribute_report.append(adversaries_dict)
      return threat_attribute_report


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
    CONNECTOR_NAME = 'ThreatQ_Connector'
    data_source['id'] = CONNECTOR_NAME

    # Add Namespace
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

    pattern = self.get_pattern_from_json(json_data)
    external_reference = self.get_external_reference_from_json(json_data)
    indicator_types = self.get_optional_values(json_data)
    description = self.get_description(json_data)
    threat_score = self.get_threat_score(json_data, indicator_types)
    threat_attributes = self.get_threat_attributes(json_data)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)
    # END PROPERTIES

    # Append to stix map json
    # Convert to function
    if (len(json_data['report']) == 0):
      json_data['report'] = [{'message': 'IOC not found'}]


    # Create STIX Bundle and add SDOs
    sdo_translator_object = sdo_translator.SdoTranslator(self.options)
    stix_bundle = sdo_translator_object.create_stix_bundle()

    # Add Indentity SDO
    identity_object = sdo_translator_object.create_identity_sdo(data_source, NAMESPACE)
    stix_bundle['objects'] += identity_object

    # Add extension-definition SDO
    toplevel_properties = ['x_ibm_original_threat_feed_data', 'threat_score']
    nested_properties = []
    if (threat_attributes):
      toplevel_properties.append('threat_attributes')
    # extension property to get the attribute list from the enrich info

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if threat_attributes:
      top_indicator.append(threat_attributes)


    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object


    # data = json.dumps(json_data)
    # data = "[" + data + "]"
    # json_data = json.loads(data)


    # Add Infrastructure SDO
    # infrastructure_object = self.infrastructure_from_report_attributes(json_data);    
    # infrastructure_stix_object = sdo_translator_object.create_infrastructure_object_sdo(infrastructure_object, pattern['pattern'], indicator_stix_object[0]['id'])    
    # stix_bundle['objects'] += infrastructure_stix_object 

    # Add Malware SDO
    # malware_object = self.malware_from_report_attributes(json_data);    
    # print('xyz')
    # malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object, indicator_stix_object[0]['id'], pattern['pattern'])
    # stix_bundle['objects'] += malware_stix_object

    return stix_bundle

