from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes, evaluate_attribute_type
from os import path
import json
from ipaddress import ip_network, IPv4Network, IPv6Network, IPv6Network
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
    if value in ["KNOWN", 'known']:
      return 'benign'
    elif value in ['suspicious', 'SUSPICIOUS']:
      return 'anomalous-activity'
    elif value in ['malicious', 'MALICIOUS']:
      return 'malicious-activity'
    # if key/value pair is not included in the XFE report
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

  #return optional fields for indicators such as name, description, indicator-type, kill-chain-phases etc
  def get_optional_values(self, data):

    for ds_key in data:
      if ds_key == "rl":
        if "malware_presence" in data[ds_key][0]:
          if 'status' in data[ds_key][0]['malware_presence']:
            value = data[ds_key][0]['malware_presence']['status']
            indicator_types_value = self.get_indicator_types(value)
            indicator_types = {
              "indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
            return indicator_types

        elif data[ds_key][0].get('classification') is not None:
          value = data[ds_key][0]['classification']
          indicator_types_value = self.get_indicator_types(value)
          indicator_types = {
            "indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
          return indicator_types

        elif 'uri_state' in data[ds_key][0]:
          counters = data[ds_key][0]['uri_state']['counters']
          if counters['malicious'] > 0 and counters['malicious'] >= counters['suspicious']:
            value = 'malicious'
          elif counters['suspicious'] > 0:
            value = 'suspicious'
          elif counters['known'] > 0:
            value = 'known'
          else:
            value = 'unknown'
          indicator_types_value = self.get_indicator_types(value)
          return {"indicator_types": [indicator_types_value]}

        else:
          value = 'Not Available'
          indicator_types_value = self.get_indicator_types(value)
          indicator_types = {
            "indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
          return indicator_types

    return None

  def get_description(self, data):
    if data.get('rl'):
        rl_report = data['rl'][0]
        if "uri_state" in rl_report:
          value = rl_report['uri_state']['counters']
          value = dict((k.capitalize(), v) for (k, v) in value.items())
          description = {"description": str(value).strip('{}')}
          return description

        elif "analysis" in rl_report:
          value = rl_report['analysis']['statistics']
          value = dict((k.capitalize(), v) for (k, v) in value.items())
          description = {"description":  str(value).strip('{}')}
          return description

        # elif "malware_presence" in data[ds_key][0] and (data[ds_key][0].get('malware_presence').get('classification') is not None):
        #   value = data[ds_key][0]['malware_presence']['classification']
        #   value = dict((k.capitalize(), v) for (k, v) in value.items())
        #   description = {"description":  str(value).strip('{}')}
        elif "malware_presence" in rl_report and (rl_report.get('malware_presence').get('status')):
          value = rl_report['malware_presence']['status']
          description = 'Report - {}'.format(value) 
          return {"description":  description}

        else:
          description = {"description": "Report - Not Available"}
          return description

    return {'description': 'Not Available'}

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Analyzer result JSON
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


  def get_malware_object(self, data):
    try:
    # Malware SDO only present in RL hash dataType
      if data["dataType"] == 'hash' and data['rl'][0].get('malware_presence'):
        classification = data['rl'][0]['malware_presence'].get('classification', {})
        malware = []
        malware_type = classification.get('type')
        malware_info = {}
        if malware_type:
          malware_info['malware_types'] = malware_type
          malware_info['is_family'] = True
          malware.append(malware_info)
        return malware
      else:
        return

    except ValueError:
      raise ValueError("Exception occurred to parse report data for malware SDO")

  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    report = {'x_ibm_original_threat_feed_data': {'full': data['rl']}}
    return report


  def get_threat_score(self, data, indicator):


    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    UNKNOWN_SCORE_MAX = 29
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100
    INDICATOR_TYPE = indicator['indicator_types'][0]

    if(INDICATOR_TYPE == 'benign'):
      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX
    elif(INDICATOR_TYPE == 'unknown'):
      tis_range_min = UNKNOWN_SCORE_MIN
      tis_range_max = UNKNOWN_SCORE_MAX
    elif (INDICATOR_TYPE == 'anomalous-activity'):
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
    else:
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX


    ds_key = data.get('rl', [])
    if ds_key:
      ds_key = ds_key[0]

      # When IP addr is passed
      if "uri_state" in ds_key:

        if(INDICATOR_TYPE == 'benign'):
          return {"threat_score": BENIGN_SCORE_MIN}
        elif (INDICATOR_TYPE == 'unknown'):
          return {"threat_score": UNKNOWN_SCORE_MIN}

        malicious = ds_key['uri_state']['counters']['malicious']
        suspicious = ds_key['uri_state']['counters']['suspicious']

        if malicious >= suspicious:
          threat_score = malicious/suspicious if suspicious != 0 else malicious
        else:
          threat_score = suspicious/malicious if malicious != 0 else suspicious

        range_min = 0
        range_max = 10
        if threat_score > 10:
          threat_score = 10

        tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
        return {"threat_score": round(tis_score, 1)}

      elif "analysis" in ds_key:
        statistics = ds_key['analysis']['statistics']
        malicious = statistics['malicious']
        suspicious = statistics['suspicious']
        unknown = statistics['unknown']
        known = statistics['known']

        if (malicious > 0 and malicious >= suspicious):
          threat_score = malicious/suspicious if suspicious != 0 else malicious
        elif suspicious > 0:
          threat_score = suspicious/malicious if malicious != 0 else suspicious
        elif unknown > 0:
          threat_score = int(unknown/known * 10)
        else:
          threat_score = 0

        range_min = 0
        range_max = 10
        if threat_score > 10:
          threat_score = 10
        tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
        return {"threat_score": round(tis_score, 1)}

      # When Hash is passed
      elif "malware_presence" in ds_key and 'threat_level' in ds_key['malware_presence'] and 'trust_factor' in ds_key['malware_presence']:
        threat_level = ds_key['malware_presence']['threat_level']
        trust_factor = ds_key['malware_presence']['trust_factor']
        # Since trust factor = 0 is most trustworthy, we flip the list
        trust_range = [5, 4, 3, 2, 1, 0]
        trust = trust_range[trust_factor]
        threat_score = threat_level * trust
        range_min = 0
        range_max = 25

        tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
        threat_score = {"threat_score": round(tis_score, 1)}
        return threat_score

    return {"threat_score": round(tis_range_min, 1)}


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    if 'rl' not in data:
      return {'threat_attributes' : threat_attribute_report}

    full_report = data.get('rl', [])[0]
    # We pass the fields we want as attributes, with then new names of the fields
    
    uri_state_fields = { 'sha1': 'SHA-1' }
    field_dict = {'uri_state': uri_state_fields}

    for attribute_keys, attribute_value in field_dict.items():
      if full_report.get(attribute_keys):
        threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

    uri_counters = full_report.get('uri_state', {}).get('counters')
    if uri_counters:
      threat_attribute_report.extend(self.get_uri_counters_attributes(uri_counters))


    if data['dataType'] == 'hash':
      malware_presence_fields = {
        'first_seen': 'First Seen', 
        'last_seen': 'Last Seen',
        'classification': 'Classification', # Available in RF Description
        'scanner_count': 'Scanner Count',
        'scanner_percent': 'Scanner Percent',
        'scanner_match': 'Scanner Match',
        'status': 'Status',
        'threat_level': 'Threat Level',
        'trust_factor': 'Trust Factor',
      }

      classification_fields = {
        'subplatform': 'Subplatform',
        'platform': 'Platform',
        'type': 'Type',
        'is_generic': 'Is Generic',
        'family_name': 'Family Name'
      }

      field_dict = {
        'malware_presence': malware_presence_fields,
        'classification': classification_fields
      }

      for attribute_keys, attribute_value in field_dict.items():
        if attribute_keys in full_report:
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      if full_report.get('malware_presence', {}).get('classification'):
        full_report = full_report['malware_presence']
        for attribute_keys, attribute_value in field_dict.items():
          if attribute_keys in full_report:
            threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])


    elif data['dataType'] == 'url' or data['dataType'] == 'domain':
      full_fields = {
        'classification': 'classification', # Available in indicator types
      }
      THIRD_PARTY_REPUTATIONS = 'third_party_reputations'
      if full_report.get('classification'):
        attribute_dict = {}
        attribute_dict['attribute_name'] = full_fields['classification']
        attribute_dict['attribute_value'] = full_report['classification']
        attribute_dict['attribute_type'] = evaluate_attribute_type(full_report['classification'])
        threat_attribute_report.append(attribute_dict)

      if full_report.get('third_party_reputations', {}).get('statistics', {}):
        attribute_dict, statistics = {}, full_report[THIRD_PARTY_REPUTATIONS]['statistics']
        for statistics_key, statistics_value in statistics.items():
          attribute_dict = {}
          attribute_dict['attribute_name'] = THIRD_PARTY_REPUTATIONS + " {}".format(statistics_key)
          attribute_dict['attribute_value'] = statistics_value
          attribute_dict['attribute_type'] = evaluate_attribute_type(statistics_value)
          threat_attribute_report.append(attribute_dict)


    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def get_uri_counters_attributes(self, uri_counters: dict) -> list:
      threat_attribute_report = []
      for counter,value in uri_counters.items():
        attribute_name = '{} Counters'.format(counter.capitalize())
        counter_dict = {
          'attribute_name': attribute_name,
          'attribute_value': value,
          'attribute_type': evaluate_attribute_type(value)
        }
        threat_attribute_report.append(counter_dict)
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
    CONNECTOR_NAME = 'ReversingLabs_Connector'
    data_source['id'] = CONNECTOR_NAME

    # Add Namespace
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

    pattern = self.get_pattern_from_json(json_data)
    indicator_types = self.get_optional_values(json_data)
    description = self.get_description(json_data)
    threat_attributes = self.get_threat_attributes(json_data)
    threat_score = self.get_threat_score(json_data, indicator_types)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, indicator_types, description, indicator_name)

    if (len(json_data['rl']) == 0):
        json_data['rl'] = [{'message': 'IOC not found'}]


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
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attributes):
      top_indicator.append(threat_attributes)

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

    malware_object = self.get_malware_object(json_data)
    # Add Malware SDO    
    # Should return a list of malware dict
    if malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object, indicator_stix_object[0]['id'], pattern['pattern'])
      stix_bundle['objects'] += malware_stix_object

    return stix_bundle