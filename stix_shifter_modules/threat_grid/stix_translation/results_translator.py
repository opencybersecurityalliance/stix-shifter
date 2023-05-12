from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
import json
from ipaddress import ip_network, IPv4Network, IPv6Network
import uuid
from urllib.parse import urlparse
from operator import itemgetter
from copy import deepcopy

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
    try:
      threat_score = value['report']['full']['analysis_report']['threat']['threat_score']
      if threat_score >= 50 and threat_score <= 89:
        return {"indicator_types": ["anomalous-activity"]}
      elif threat_score >= 90 and threat_score <= 100:
        return {"indicator_types": ["malicious-activity"]}
      else:
        return {"indicator_types": ["benign"]}
    except:
      return {"indicator_types": ["unknown"]} 


  def find_hash_type_by_length(self, value):
    HASH_LENGTH = {'40': 'sha-1', '64': 'sha-256', '32': 'md5'}
    hash_type = HASH_LENGTH.get(str(len(value)), '')
    if hash_type in ['sha-1', 'sha-256']:
        return "file:hashes.'{}'".format(hash_type.upper())
    else:
        return "file:hashes.{}".format(hash_type.upper())


  def get_ip_address(self, ip):
    return 'ipv4' if isinstance(ip_network(ip), IPv4Network) else 'ipv6'


  def get_external_reference_from_json(self, data):
    ext_data = data['external_reference']
    if ext_data.get('url') == '' or ext_data.get('url') == 'N/A':
      return None
    url = data['external_reference']
    external_reference = {"external_references":[url]}
    return external_reference


  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Connector result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern


  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "ip", "url", "unknown"],
    if pattern_type == 'domain':
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


  def get_description(self, data):
    try:
      if data['report']['full'].get('analysis_report').get('threat'):
        suspected_categories = data['report']['full']['analysis_report']['threat'].get('suspected_categories')
        if suspected_categories[0]:
          return {"description": suspected_categories[0].capitalize()}
        return {"description": "No description"}
    except:
      return {"description": "No description"}


  def get_threat_score(self, data):

    # Declare constants
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    # Normalize the score out of 100
    try:
      if data['report']['full'].get('analysis_report').get('threat').get('threat_score') is None:
        return {"threat_score": UNKNOWN_SCORE_MIN}
    except:
        return {"threat_score": UNKNOWN_SCORE_MIN}  

    threat_score = data['report']['full']['analysis_report']['threat']['threat_score']
    threat_feed_ranges = [(0, 49), (50, 89), (90, 100)]

    tis_ranges = [(BENIGN_SCORE_MIN, BENIGN_SCORE_MAX), 
      (SUSPICIOUS_SCORE_MIN, SUSPICIOUS_SCORE_MAX), 
      (MALICIOUS_SCORE_MIN, MALICIOUS_SCORE_MAX)]

    for i in range(0, len(threat_feed_ranges)):
      if threat_score <= threat_feed_ranges[i][1]:
        range_min = threat_feed_ranges[i][0]
        range_max = threat_feed_ranges[i][1]
        tis_range_min = tis_ranges[i][0]
        tis_range_max = tis_ranges[i][1]

        tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
        return {"threat_score": round(tis_score, 1)}


  def get_malware_object(self, data):
    try:
      if data['report']['full'].get('analysis_report').get('threat'):
        suspected_categories = data['report']['full']['analysis_report']['threat'].get('suspected_categories')     

        malware = []
        malware_types = []
        malware_capabilities = []      
        malware_object= {}
        for suspect in suspected_categories:
          malware_types.append(suspect)
          if(self.evaluate_malware_capabilities(suspect)):
            malware_capabilities.append(self.evaluate_malware_capabilities(suspect))

        malware_object['is_family'] = False
        malware_object['malware_types'] = malware_types
        if len(malware_capabilities) > 0:
          malware_object['capabilities'] = malware_capabilities      
        malware.append(malware_object)        
        return malware
    except:
      return 


  def evaluate_malware_capabilities(self, value):
    if value == 'banking' or value == 'data-theft' or value == 'exfiltration':
      return 'exfiltrates-data'
    if value == 'pua':
      return 'installs-other-components'
    if value == 'anti-analysis':
      return 'evades-av'
    if value == 'anti-forensics':
      return 'anti-memory-forensics'
    if value == 'persistence':
      return 'persists-after-system-reboot'
    if value == 'weakening':
      return 'degrades-security-software'
    if value == 'evasion':
      return 'hides-artifacts'


  def get_infrastructure_object(self, data):
    if data['report']['full'].get('analysis_report', {}).get('threat'):
      suspected_categories = data['report']['full']['analysis_report']['threat'].get('suspected_categories')
      infrastructure = {'infrastructure_types': []}
      for suspect in suspected_categories:
        infra_type = suspect
        if infra_type is not None and infra_type not in infrastructure['infrastructure_types']:
          infrastructure['infrastructure_types'].append(infra_type)
      return infrastructure
    else:
      return None


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if type(prop) is dict:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    malware_descriptions = []
    if 'report' in data:

      full_fields = {
        'host': 'ThreatGrid Host',
        'sample_id': 'ThreatGrid Sample ID',
      }
      
      submission_fields = { 'total': 'Total Samples' }

      field_dict = { 'full': full_fields }
      full_report = data['report']

      for attribute_keys, attribute_value in field_dict.items():
        if attribute_keys in full_report:
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      full_report = data['report'].get('full', {})

      malware_descriptions = full_report.get('analysis_report', {}).get('metadata', {}).get('malware_desc', [])

      # Loop through metadata array in analysis_report.metadata.malware_desc
      if malware_descriptions:
        threat_attribute_report.extend(self.get_malware_attributes(malware_descriptions))

      submission_report = full_report.get('submission_data')
      if submission_report:
        threat_attribute_report.extend(self.get_submission_attributes(submission_fields, submission_report))

        behaviors_report = submission_report.get('item', {}).get('analysis', {}).get('behaviors')
        if behaviors_report:
          threat_attribute_report.extend(self.get_behavior_attributes(behaviors_report))

    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  # We create a new function to reduce cognitive complexity in function get_threat_attributes()
  def get_malware_attributes(self, malware_descriptions) -> list:
    malware_fields = ['filename', 'type', 'sha1', 'sha256', 'md5']
    threat_attribute_report = []
    for index, malware in enumerate(malware_descriptions):
      for field in malware_fields:
        malware_string = malware.get(field)
        if malware_string:
          attribute_name = 'Malware Description {} {}'.format(index+1, field)
          malware_dict = {
            'attribute_name': attribute_name,
            'attribute_value': malware_string,
            'attribute_type': 'string'
          }
          threat_attribute_report.append(malware_dict)
    return threat_attribute_report


  def get_submission_attributes(self, submission_fields, submission_report) -> list:
    threat_attribute_report = []
    for attribute_keys, attribute_value in submission_fields.items():
      if attribute_keys in submission_report:
        threat_attribute_report += create_attributes(attribute_value, submission_report[attribute_keys])
    return threat_attribute_report


  def get_behavior_attributes(self, behaviors_report):
    '''
      from submission_data.analysis.behaviors
      we take the first 5 behaviors with threat score >= 95 and display the remaining as an int
      if we have less than 5 behaviors we list all of them
      if we have greater than 5 behaviors but not all of them are >= 95 than we only display the ones that are
    '''

    # Sort behaviors by threat in desc order
    behaviors = sorted(behaviors_report, key=itemgetter('threat'), reverse=True)
    behavior_attributes = []

    # SHOW ALL if <= 5
    if len(behaviors) <= 5: return [self.create_behaviors_dict(behaviors)] 

    # If none are >= 95 then we display first 5
    if behaviors[0]['threat'] < 95: return [self.create_behaviors_dict(behaviors, behaviors[0:5])]

    # Display only first 5 or less behavior(Score) with threat >= 95
    for behavior in behaviors:
      if behavior['threat'] < 95 or len(behavior_attributes) == 5: break
      behavior_attributes.append(behavior)

    behaviors_dict = self.create_behaviors_dict(behaviors, behavior_attributes)

    return [behaviors_dict]


  def create_behaviors_dict(self, behaviors: list, behavior_attributes=None) -> dict:
    names = ''
    remainder = '' if len(behaviors) <= 5 else ' and {} more'.format(len(behaviors) - len(behavior_attributes))
    
    if behavior_attributes:
      for behavior in behavior_attributes:
        names += '{} ({}), '.format(behavior['name'], behavior['threat'])

    else:
      for behavior in behaviors:
        names += '{} ({}), '.format(behavior['name'], behavior['threat'])
    
    
    names = names[:-2] # Get rid of ', ' at the end
    value = names + remainder
    behaviors_dict = {
      'attribute_name': 'Behaviors (Score)',
      'attribute_value': value,
      'attribute_type': evaluate_attribute_type(value)
    }
    
    return behaviors_dict

  def get_threat_report(self, data):
    return {'x_ibm_original_threat_feed_data': data['report']}


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
    data_type = json_data['dataType']
    CONNECTOR_NAME = 'ThreatGrid_Connector'
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
    indicator_types = self.get_indicator_types(json_data) #obtain from report
    description = self.get_description(json_data) #obtain from report
    threat_score = self.get_threat_score(json_data)
    threat_attributes = self.get_threat_attributes(json_data)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)
    malware_object = self.get_malware_object(json_data)
    infrastructure_object = self.get_infrastructure_object(json_data)

    full_report = deepcopy(json_data)
    full_report['report']['full'] = [full_report['report']['full']]


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

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    report = self.get_threat_report(full_report)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attributes):
      top_indicator.append(threat_attributes)

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

    # Add Malware SDO    
    # Should return a list of malware dict
    if malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object, indicator_stix_object[0]['id'], pattern['pattern'])
      stix_bundle['objects'] += malware_stix_object

    # Add infrastructure object
    if infrastructure_object and (len(infrastructure_object['infrastructure_types']) > 0) and (data_type in ('ip','url', 'domain')):      
      infrastructure_stix_object = sdo_translator_object.create_infrastructure_object_sdo(infrastructure_object, pattern['pattern'], indicator_stix_object[0]['id'])
      stix_bundle['objects'] += infrastructure_stix_object


    return stix_bundle
