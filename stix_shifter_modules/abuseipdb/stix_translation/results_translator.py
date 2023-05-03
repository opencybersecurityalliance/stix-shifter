from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
import json
from ipaddress import ip_network, IPv4Network, IPv6Network
import uuid
from urllib.parse import urlparse
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
    if (value>=0 and value<=25):
      return 'benign'
    elif (value>=26 and value<=74):
      return 'anomalous-activity'
    elif (value>=75 and value<=100):
      return 'malicious-activity'
    # if key/value pair is not included in the report
    elif value is None:
      return 'unknown'
    else:
      return 'unknown'

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
  def get_optional_values(self, value):    
    indicator_types_value = self.get_indicator_types(value)
    indicator_types = {"indicator_types": [indicator_types_value]} if indicator_types_value is not None else None
    return indicator_types

  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Analyzer result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern

  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "ip", "url", "unknown"],
    if pattern_type == 'ip':
      pattern_type = self.get_ip_address(value)
      pattern = "["+ pattern_type + "-addr:value='" + value + "']"
      return pattern

    return pattern

  def get_threat_score(self, threat_score):
    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    if threat_score is None:
      return {"threat_score": UNKNOWN_SCORE_MIN}

    # Declare constants

    range_min = 0
    range_max = 100

    if(threat_score>=0 and threat_score<=25):
      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    elif (threat_score>=26 and threat_score<=74):
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    elif (threat_score>=75 and threat_score<=100):
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    else:
      tis_score = UNKNOWN_SCORE_MIN  

    if tis_score > range_max:
      tis_score = range_max  

    threat_score = {"threat_score": round(tis_score, 1)}
    
    return threat_score

  def get_description(self, score):
    indicator_type = self.get_indicator_types(score)
    description = "IP is following into " + indicator_type + " category"
    return {"description": description}


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
      full_report = data['report'][0]
      full_fields = {
        'ipAddress': 'IP Address',
        'isPublic': 'Is Public',
        'isWhitelisted': 'Is Whitelisted',
        'totalReports': 'Total Reports',
        'numDistinctUsers': 'Number of Distinct Users',
        'lastReportedAt': 'Last Reported At',
        'usageType': 'Usage Type',
        'domain': 'Domain'
      }

      for attribute_keys, attribute_value in full_fields.items():
        if attribute_keys in full_report:
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

    ANALYZER_NAME = "AbuseIPDB_Connector"
    data_source['id'] = ANALYZER_NAME

    # Add Namespace
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = ANALYZER_NAME
    pattern = self.get_pattern_from_json(json_data)
    external_reference = self.get_external_reference_from_json(json_data)
    indicator_types = self.get_optional_values(json_data['report'][0]['abuseConfidenceScore'])
    description = self.get_description(json_data['report'][0]['abuseConfidenceScore'])
    threat_score = self.get_threat_score(json_data['report'][0]['abuseConfidenceScore'])
    threat_attributes = self.get_threat_attributes(json_data)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)

    #json_data['report']['full'] = json_data['report']	


    # Create STIX Bundle and add SDOs
    sdo_translator_object = sdo_translator.SdoTranslator(self.options)
    stix_bundle = sdo_translator_object.create_stix_bundle()


    # Add Identity SDO
    identity_object = sdo_translator_object.create_identity_sdo(data_source, NAMESPACE)
    stix_bundle['objects'] += identity_object

    # Add extension-definition SDO
    toplevel_properties = ['x_ibm_original_threat_feed_data', 'threat_score']
    if (threat_attributes):
      toplevel_properties.append('threat_attributes')
    # extension property to get the attribute list from the enrich info
    nested_properties = []

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

    return stix_bundle