from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
from ipaddress import ip_network, IPv4Network
import uuid

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
    for ds_key in data:
      if ds_key == "rl":

        if "uri_state" in data[ds_key][0]:
          value = data[ds_key][0]['uri_state']['counters']
          description = {"description": str(value).strip('{}')}
          return description

        elif "analysis" in data[ds_key][0]:
          value = data[ds_key][0]['analysis']['statistics']
          description = {"description":  str(value).strip('{}')}
          return description

        elif "malware_presence" in data[ds_key][0] and (data[ds_key][0].get('malware_presence').get('classification') is not None):
          value = data[ds_key][0]['malware_presence']['classification']
          description = {"description":  str(value).strip('{}')}
          return description

        else:
          description = {"description": "Not Available"}
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
      if data["dataType"] == 'hash' and data['rl'][0].get('malware_presence') and data['rl'][0]['malware_presence'].get('classification'):
        classification = data['rl'][0]['malware_presence'].get('classification')
        malware = []
        malware_type = classification.get('type')
        #malware_family = classification.get('family_name')
        malware_info = {}
        if malware_type:
          malware_info['malware_types'] = malware_type
          #malware_info[]
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
    if not indicator:
      return None

    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    UNKNOWN_SCORE_MAX = 29
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    for ds_key in data:
      if ds_key == "rl":
        # When IP adr is passed
        if "uri_state" in data[ds_key][0]:

          if(indicator['indicator_types'][0] == 'benign'):
            return {"threat_score": 0.0}
          elif (indicator['indicator_types'][0] == 'unknown'):
            return {"threat_score": UNKNOWN_SCORE_MIN}

          malicious = data[ds_key][0]['uri_state']['counters']['malicious']
          suspicious = data[ds_key][0]['uri_state']['counters']['suspicious']

          if malicious >= suspicious:
            tis_range_min = MALICIOUS_SCORE_MIN
            tis_range_max = MALICIOUS_SCORE_MAX
            threat_score = malicious/suspicious if suspicious != 0 else malicious
          else:
            tis_range_min = SUSPICIOUS_SCORE_MIN
            tis_range_max = SUSPICIOUS_SCORE_MAX
            threat_score = suspicious/malicious if malicious != 0 else suspicious

          range_min = 1
          range_max = 10
          if threat_score > 10:
            threat_score = 10
          tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
          return {"threat_score": round(tis_score, 1)}

        elif "analysis" in data[ds_key][0]:
          statistics = data[ds_key][0]['analysis']['statistics']
          malicious = statistics['malicious']
          suspicious = statistics['suspicious']
          unknown = statistics['unknown']
          known = statistics['known']
          if (malicious > 0 and malicious >= suspicious):
            tis_range_min = MALICIOUS_SCORE_MIN
            tis_range_max = MALICIOUS_SCORE_MAX
            threat_score = malicious/suspicious if suspicious != 0 else malicious
          elif suspicious > 0:
            tis_range_min = SUSPICIOUS_SCORE_MIN
            tis_range_max = SUSPICIOUS_SCORE_MAX
            threat_score = suspicious/malicious if malicious != 0 else suspicious
          elif unknown > 0:
            tis_range_min = UNKNOWN_SCORE_MIN
            tis_range_max = UNKNOWN_SCORE_MAX
            threat_score = int(unknown/known * 10)
          else:
            return {"threat_score": 0.0}
          range_min = 1
          range_max = 10
          if threat_score > 10:
            threat_score = 10
          tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
          return {"threat_score": round(tis_score, 1)}

        # When Hash is passed
        elif "malware_presence" in data[ds_key][0] and 'threat_level' in data[ds_key][0]['malware_presence'] and 'trust_factor' in data[ds_key][0]['malware_presence']:
          threat_level = data[ds_key][0]['malware_presence']['threat_level']
          trust_factor = data[ds_key][0]['malware_presence']['trust_factor']
          # Since trust factor = 0 is most trustworthy, we flip the list
          trust_range = [5, 4, 3, 2, 1, 0]
          trust = trust_range[trust_factor]
          threat_score = threat_level * trust
          range_min = 0
          range_max = 25
          if(indicator['indicator_types'][0] == 'benign'):
            tis_range_min = BENIGN_SCORE_MIN
            tis_range_max = BENIGN_SCORE_MAX
            tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
          elif(indicator['indicator_types'][0] == 'unknown'):
            tis_range_min = UNKNOWN_SCORE_MIN
            tis_range_max = UNKNOWN_SCORE_MAX
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

        else:
          if(indicator['indicator_types'][0] == 'benign'):
            return {"threat_score": round(BENIGN_SCORE_MIN, 1)}
          elif(indicator['indicator_types'][0] == 'unknown'):
            return {"threat_score": round(UNKNOWN_SCORE_MIN, 1)}
          elif(indicator['indicator_types'][0] == 'anomalous-activity'):
            return {"threat_score": round(SUSPICIOUS_SCORE_MIN, 1)}
          else:
            return {"threat_score": round(MALICIOUS_SCORE_MIN, 1)}


  def translate_results(self, data_source, data):
    """
    Translates JSON data into STIX results
    :param data: JSON formatted data to translate into STIX format
    :type data: str
    :return: STIX formatted results
    :rtype: str
    """

    json_data = data
    json_data = json_data[0]
    ANALYZER_NAME = 'ReversingLabs_1_0'
    data_source['id'] = ANALYZER_NAME

    # Add Namespace
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = ANALYZER_NAME

    pattern = self.get_pattern_from_json(json_data)
    indicator_types = self.get_optional_values(json_data)
    description = self.get_description(json_data)
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
    toplevel_properties = ['x_ibm_original_threat_feed_data']
    nested_properties = []
    if (threat_score):
      toplevel_properties.append('threat_score')

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties=toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    extension_id = extension_object[0]['id']
    identity_id = identity_object[0]['id']
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]

    indicator_stix_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_stix_object

    malware_object = self.get_malware_object(json_data)
    # Add Malware SDO    
    # Should return a list of malware dict
    if malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object, indicator_stix_object[0]['id'], pattern['pattern'])
      stix_bundle['objects'] += malware_stix_object

    return stix_bundle