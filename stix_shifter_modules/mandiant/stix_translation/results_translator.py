from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
from os import path
import json
from ipaddress import ip_network, IPv4Network
from stix_shifter_utils.utils import logger
import uuid

def findkeys(node, key):
  if hasattr(node, 'items'):
    for k, v in node.items():
      if k == key and v:
        yield v
      if isinstance(v, dict):
        for r in findkeys(v, key):
          yield r
      elif isinstance(v, list):
        for i in v:
          for r in findkeys(i, key):
            yield r
  elif isinstance(node, list):
    for m in node:
      for n in findkeys(m, key):
        yield n
class ResultsTranslator(BaseResultTranslator):

  # Get indicator_types value
  def get_indicator_types(self, data):
    verdicts = data['report']['full'].get('verdict')
    if verdicts is None: 
      return {"indicator_types": ['unknown']}
    else:  
      mandiant_score = data['report']['full'].get('mscore')
      # authoritative_verdict = verdicts.get('authoritativeVerdict', None)
      # indicator_type = verdicts[authoritative_verdict].get('verdict', 'unknown')
      if mandiant_score <= 40: indicator_type = 'benign'
      elif mandiant_score < 60: indicator_type = 'anomalous-activity'
      else: indicator_type = 'malicious-activity'

      return {"indicator_types": [indicator_type]}

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
    data_type = data['report']['full'].get('type')
    value = data['report']['full'].get('value')

    if data_type is None or value is None: return None

    external_ref = f"https://advantage.mandiant.com/indicator/{data_type}/{value}"
    external_reference = {"external_references": [{"source_name": "Mandiant_Connector", "url": external_ref}]}
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


  def get_description(self, data):
    verdicts = data['report']['full'].get('verdict', None)
    if verdicts is None:
      return {"description": "N/A"}
    else:
      malicious_count = 0
      benign_count = 0
      src_set = set()
      for k, v in verdicts.items():
        if isinstance(v, dict):
          reasoning = v.get('reasoning', None)
          if reasoning is not None:  
            m_cnt = reasoning.get('malicious_count')
            b_cnt = reasoning.get('benign_count')
            if m_cnt and m_cnt > 0:
              malicious_count += m_cnt
              src_set.add(k)
            if b_cnt and b_cnt > 0:
              benign_count += b_cnt
              src_set.add(k)    
      
      src_list = ''
      for s in src_set:
          src_list = src_list + ', ' + s
      src_list = src_list[2:]
      description = f"{malicious_count} Malicious and {benign_count} Benign responses came from {malicious_count + benign_count} sources: {src_list}"
      return {"description": description}


  def get_threat_score(self, data, indicator):
    if not indicator:
      return None

    threat_score = data['report']['full'].get('mscore', 0)

    # Declare constants
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    UNKNOWN_SCORE_MAX = 29
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    range_min = 0
    range_max = threat_score if threat_score >= 10 else 10

    if(indicator['indicator_types'][0] == 'benign'):
      range_min = 0
      range_max = 40
      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    elif(indicator['indicator_types'][0] == 'unknown'):
      tis_range_min = UNKNOWN_SCORE_MIN
      tis_range_max = UNKNOWN_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    elif (indicator['indicator_types'][0] == 'anomalous-activity'):
      range_min = 41
      range_max = 59
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    else:
      range_min = 60
      range_max = 100
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    threat_score = {"threat_score": round(tis_score, 1)}
    
    return threat_score


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    return {'x_ibm_original_threat_feed_data': data['report']}

  def get_threat_attributes(self, data):    
    misp = data['report']['full'].get('misp', None)
    if misp is None: 
      return None
    else:  
      value = ''
      for k, v in misp.items():
        if v == True:
          value = value + ', ' + k
      
      if value == '':
        return None
      else:
        value = value[2:]
        attr_obj = dict()
        attr_obj['attribute_name'] = 'Threat Feeds'
        attr_obj['attribute_value'] = value
        attr_obj['attribute_type'] = 'string'
        return {'threat_attributes': [attr_obj]}
    

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
    CONNECTOR_NAME = "Mandiant_Connector"
    data_source['id'] = "MandiantConnector"

    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

    pattern = self.get_pattern_from_json(json_data)
    external_reference = self.get_external_reference_from_json(json_data)
    indicator_types = self.get_indicator_types(json_data) #get indicator types from the report
    description = self.get_description(json_data) #get description from the report
    threat_score = self.get_threat_score(json_data, indicator_types)
    threat_attrs = self.get_threat_attributes(json_data)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)
    json_data['report']['full'] = [json_data['report']['full']]

      # Create STIX Bundle and add SDOs
    sdo_translator_object = sdo_translator.SdoTranslator(self.options)
    stix_bundle = sdo_translator_object.create_stix_bundle()


    # Add Indentity SDO
    identity_object = sdo_translator_object.create_identity_sdo(data_source, NAMESPACE)
    stix_bundle['objects'] += identity_object

    # Add extension-definition SDO
    toplevel_properties = ['x_ibm_original_threat_feed_data', 'threat_score']
    nested_properties = []
    if (threat_attrs):
      toplevel_properties.append('threat_attributes')

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attrs):
      top_indicator.append(threat_attrs)

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

    return stix_bundle
