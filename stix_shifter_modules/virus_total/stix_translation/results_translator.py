from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
import json
from stix_shifter_utils.utils.file_helper import read_json as helper_read_json
from ipaddress import ip_network, IPv4Network, IPv6Network
import uuid
from urllib.parse import urlparse
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

  def get_indicator_types(self, value):
    if value == 'safe':
        return 'benign'
    elif value == 'suspicious':
        return 'anomalous-activity'
    elif value == 'malicious':
        return 'malicious-activity'
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

  # Get permalink from the report
  def get_external_reference_from_json(self, data):
    ext_data = data['external_reference']
    if ext_data.get('url') == '' or ext_data.get('url') == 'N/A':
      return None
    url = data['external_reference']
    external_reference = {"external_references":[url]}
    return external_reference

  #return optional fields for indicators such as name, description, indicator-type, kill-chain-phases etc
  def get_optional_values(self, data):
    data_detail = self.get_details(data['report']['full']) if data['report']['full'] else None
    if data_detail:   
      indicator_types_value = self.get_indicator_types(data_detail['criticality']) if 'criticality' in data_detail else None
      indicator_types = {"indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
      return indicator_types
    else:
      return {"indicator_types": ['unknown']}

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Transmission result JSON
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


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    return {'x_ibm_original_threat_feed_data': data['report']}


  def get_infrastructure_object(self,data):
    try:
      infra_attributes={}
      infra_type=[]

      # URL handling
      if 'data' in data['report']['full'] and 'attributes' in data['report']['full']['data'] and data['dataType'] == 'url':
        if 'last_analysis_results' in data['report']['full']['data']['attributes']:
          scans = data['report']['full']['data']['attributes']['last_analysis_results']
          for scan in scans:
            word = scans[scan]['result'].split()[0]
            word = 'hosting-malware' if word in ['malware', 'malicious'] else word
            if word not in ['clean', 'unrated'] and word not in infra_type:
              infra_type.append(word)

        if (len(infra_type) > 0):
          infra_attributes['infrastructure_types'] = infra_type
      return infra_attributes
    except ValueError:
      raise ValueError("Exception occurred to parse report data for Infrastructure SDO")


  def get_malware_object(self,data):
    try:
      malware_object = {}
      # Malware SDO only present in VT Hash dataType
      if 'data' in data['report']['full'] and 'attributes' in data['report']['full']['data'] and data['dataType'] == 'hash':
        if 'last_analysis_results' in data['report']['full']['data']['attributes'] or ('popular_threat_classification' in  data['report']['full']['data']['attributes'] and 'popular_threat_category' in  data['report']['full']['data']['attributes']['popular_threat_classification']):
          word_list = []
          if 'last_analysis_results' in data['report']['full']['data']['attributes']:
            scans = data['report']['full']['data']['attributes']['last_analysis_results']
            for scan in scans:
              word = scans[scan]['result'].lower() if scans[scan]['result'] is not None else None
              if word is None:
                continue
              word_list.append(word)
          if ('popular_threat_classification' in  data['report']['full']['data']['attributes'] and 'popular_threat_category' in  data['report']['full']['data']['attributes']['popular_threat_classification']):
            scans = data['report']['full']['data']['attributes']['popular_threat_classification']['popular_threat_category']
            for scan in scans:
              word = scan['value'].lower() if scan['value'] is not None else None
              if word is None:
                continue
              word_list.append(word)
        else:
          return None
      else:
        return None

      malware_types = []
      
      for malware in word_list:
        if malware not in malware_types:
          malware_types.append(malware)
      if len(malware_types) > 0:
        malware_object['malware_types'] = malware_types
      return [malware_object]
    except ValueError:
      raise ValueError("Exception occurred to parse report data for malware SDO")

  def get_details(self, raw):
    if raw.get('data') is None:
      return []

    details = dict()
    criticality = 'info'
    last_analysis_stats = raw["data"]["attributes"]["last_analysis_stats"]
    total_detector = last_analysis_stats["malicious"] + last_analysis_stats["suspicious"] + last_analysis_stats["harmless"]  + last_analysis_stats["undetected"] + last_analysis_stats["timeout"]
    score = 0
    if (last_analysis_stats["malicious"] > 0 and last_analysis_stats["suspicious"] > 0):
      if (last_analysis_stats["malicious"] > 5 or last_analysis_stats["malicious"] > last_analysis_stats["suspicious"]):
        criticality = 'malicious'
        score = last_analysis_stats["malicious"]
      else:
        criticality = 'suspicious'
        score = last_analysis_stats["suspicious"]
    elif last_analysis_stats["malicious"] > 0:
      criticality = 'malicious'
      score = last_analysis_stats["malicious"]
    elif last_analysis_stats["suspicious"] > 0:
      criticality = 'suspicious'
      score = last_analysis_stats["suspicious"]
    elif last_analysis_stats["malicious"] == 0 and  last_analysis_stats["suspicious"] == 0 and  last_analysis_stats["undetected"] == 0:
      criticality = 'safe'

    details["criticality"] = criticality         
    details["score"] = '{}/{}'.format(score, total_detector)

    return details

  def get_description(self, data):
    data_details = self.get_details(data['report']['full']) if data['report']['full'] else None    
    description = 'N/A'
    if data_details:
        description = "{}: {}".format('Score', data_details.get('score'))

    return {"description": description}

  def get_threat_score(self, data, indicator):
    if not indicator:
      return None

    # Declare constants
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    if indicator['indicator_types'][0] == 'benign':
      return {"threat_score": BENIGN_SCORE_MIN}

    if indicator['indicator_types'][0] == 'unknown':
      return {"threat_score": UNKNOWN_SCORE_MIN}

    last_analysis_stats = data['report']['full']["data"]["attributes"]["last_analysis_stats"]

    danger_detector = 0
    score_ratio = 0

    if indicator['indicator_types'][0] == 'anomalous-activity':
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
      danger_detector = last_analysis_stats["suspicious"]

    if indicator['indicator_types'][0] == 'malicious-activity':
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
      danger_detector = last_analysis_stats["malicious"]

    total_detector = last_analysis_stats["malicious"] + last_analysis_stats["suspicious"] + last_analysis_stats["harmless"]  + last_analysis_stats["undetected"] + last_analysis_stats["timeout"]     

    
    tis_score = (tis_range_min + ((tis_range_max-tis_range_min) * (danger_detector/total_detector)))
    tis_score = round(tis_score, 1)
    if tis_score > tis_range_max:
      tis_score = tis_range_max

    return {"threat_score": tis_score}


  def get_threat_attributes(self, data):
    threat_attribute_report = []

    if 'report' in data:
      full_report = data['report'].get('full', {}).get('data', {}) # We care about data.attributes and data.info

      info_fields = {
        'positives': 'Positives',
        'total': 'Total',
        'md5': 'MD5',
        'sha1': 'SHA-1',
        'sha256': 'SHA-256',
        'resource': 'Resource',
        'scan_date': 'Scan Date',
        'scan_id': 'Scan ID',
      }

      attribute_fields = {
        'last_http_response_code': 'Last HTTP Response Code',
        'registrar': 'Domain Registrar'
      }

      field_dict = { 
        'info': info_fields,
        'attributes': attribute_fields
      }

      for attribute_keys, attribute_value in field_dict.items():
        if attribute_keys in full_report:
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      if full_report.get('info', {}).get('detected_urls'):
        detected_report = full_report.get('info', {}).get('detected_urls')
        for attribute_keys, attribute_value in info_fields.items():
          if attribute_keys in detected_report:
            threat_attribute_report += create_attributes(attribute_value, detected_report[attribute_keys])


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

    CONNECTOR_NAME = "VirusTotal_Connector"
    data_source['id'] = CONNECTOR_NAME
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
    infrastructure_object = self.get_infrastructure_object(json_data)
    malware_object = self.get_malware_object(json_data)

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


    if malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object, indicator_stix_object[0]['id'], pattern['pattern'])
      stix_bundle['objects'] += malware_stix_object

    # Add infrastructure object
    if infrastructure_object and (len(infrastructure_object['infrastructure_types']) > 0):
      infrastructure_stix_object = sdo_translator_object.create_infrastructure_object_sdo(infrastructure_object, pattern['pattern'], indicator_stix_object[0]['id'])
      stix_bundle['objects'] += infrastructure_stix_object


    return stix_bundle