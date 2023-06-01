from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
from os import path
import json
from stix_shifter_utils.utils import logger
from datetime import date, timedelta
from math import log10
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
  # Get indicator_types value
  def get_indicator_types(self, value):
    try:
      if not ('threatfeedscount' in value['report']['full'] and 
      'count' in value['report']['full']['ioc_report'] and
      'attacks' in value['report']['full']['ioc_report']):
        return {"indicator_types": ["unknown"]}
      # check if there is any actionable threatfeed
      if value['report']['full'].get('threatfeedscount') > 1:
        lastsevendays = 0
        for threatfeed in value['report']['full']['ioc_report']['threatfeeds']:
          lastseen = value['report']['full']['ioc_report']['threatfeeds'].get(threatfeed).get('lastseen')
          lastseendate = date.fromisoformat(lastseen)
          weekago = date.today() - timedelta(days = 7)
          if lastseendate > weekago:
            lastsevendays += 1
            if lastsevendays >2:
              return {"indicator_types": ["malicious-activity"]}
      if 'maxrisk' in value['report']['full']['ioc_report'] and value['report']['full']['ioc_report']['maxrisk']==0:
        return {"indicator_types": ["benign"]}
      return {"indicator_types": ["anomalous-activity"]}  
    except:
      return {"indicator_types": ["unknown"]}

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


  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Connector result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = self.evaluate_pattern(pattern_type, pattern_value)
    pattern = {"pattern": pattern}
    return pattern

  def evaluate_pattern(self, pattern_type, value):
    pattern = []
    #  "dataTypeList": ["file", "hash", "domain", "ip", "url", "unknown"],

    # Get ipv4 or ipv6
    if pattern_type == 'ip':
      pattern_type = self.get_ip_address(value)
      pattern = "["+ pattern_type + "-addr:value='" + value + "']"
      return pattern

    return pattern


  def get_description(self, data):
    try:
      if (data['report']['full']['ioc_report']):
        attacks = data['report']['full']['ioc_report'].get('attacks')
        threatfeed = data['report']['full'].get('threatfeedscount')    
        description = f"Threatfeed: {threatfeed}, Attack: {attacks} "
        return {"description": description}

    except:
      return {"description": "No description"}



  def get_threat_score(self, data, indicator):
    if not indicator:
      return None

    BENIGN_SCORE_MIN = 0
    BENIGN_SCORE_MAX = 9
    UNKNOWN_SCORE_MIN = 10
    SUSPICIOUS_SCORE_MIN = 30
    SUSPICIOUS_SCORE_MAX = 69
    MALICIOUS_SCORE_MIN = 70
    MALICIOUS_SCORE_MAX = 100

    if(indicator['indicator_types'][0] == 'unknown'):	
      return {"threat_score": UNKNOWN_SCORE_MIN}	


    attacks = data['report']['full']['ioc_report']['attacks']
    if not attacks:
      return {"threat_score": UNKNOWN_SCORE_MIN}

    threat_score = 2*log10(attacks)+data['report']['full'].get('threatfeedscount')

    if threat_score > 20:
      threat_score = 20
    range_max = 20

    if(indicator['indicator_types'][0] == 'anomalous-activity'):
      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
    elif(indicator['indicator_types'][0] == 'malicious-activity'):
      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
    elif(indicator['indicator_types'][0] == 'benign'):
      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX      

    tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score) / (range_max)
    return {"threat_score": round(tis_score, 1)}


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      for key, value in prop.items():
        indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    return {'x_ibm_original_threat_feed_data': data['report']}


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    if 'report' in data:
      full_report = data['report'].get('full', {}).get('ioc_report', {})
      # We pass the fields we want as attributes, with then new names of the fields
      attribute_fields = {
        'mindate': 'First Seen', 
        'maxdate': 'Last Seen', 
        'attacks': 'Attacks', # Number
        'ascountry': "Country", 
        'count': 'Count',
        'as': 'AS Number',
        'asname': 'AS Name', 
        'updated': 'Last Updated', 
        'network': 'Network', 
      }
      threat_attribute_report = create_attributes(attribute_fields, full_report)

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

    self.logger = logger.set_logger(__name__)

    json_data = data[0]

    CONNECTOR_NAME = 'DShield_Connector'
    data_source['id'] = CONNECTOR_NAME
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

    pattern = self.get_pattern_from_json(json_data)
    external_reference = self.get_external_reference_from_json(json_data)
    indicator_types = self.get_indicator_types(json_data)  #obtain from the report
    description = self.get_description(json_data) #obtain from the report
    threat_score = self.get_threat_score(json_data, indicator_types)
    indicator_name = {'name': json_data['data']}
    threat_attributes = self.get_threat_attributes(json_data)
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)

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

    return stix_bundle
