from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
import json
import re
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

  def get_indicator_types(self, data):
    return {"indicator_types": ['unknown']}


  def get_ip_address(self, ip):
    return 'ipv4' if isinstance(ip_network(ip), IPv4Network) else 'ipv6'


  #Get permalink from the report
  def get_external_reference_from_json(self, data):
    ext_data = data.get('external_reference')
    if ext_data.get('url') == '' or ext_data.get('url') == 'N/A':
      return None
    url = ext_data
    external_reference = {"external_references":[url]}
    return external_reference


  # Get required pattern field from the report, the pattern is a combination of data and dataType fields in the Connector result JSON
  def get_pattern_from_json(self, data):
    pattern_type, pattern_value = data['dataType'], data['data']
    pattern = {"pattern": self.evaluate_pattern(pattern_type, pattern_value)}
    return pattern


  def evaluate_pattern(self, pattern_type, value):
    pattern = None
    # Get ipv4 or ipv6
    if pattern_type == 'ip':
      pattern_type = self.get_ip_address(value)
      pattern = "["+ pattern_type + "-addr:value='" + value + "']"

    return pattern
    

  def get_description(self, data):
    c = data.get('report', {}).get('full', {}).get('country', {}).get('names', {}).get('en','')
    asn = data.get('report', {}).get('full', {}).get('traits', {}).get('autonomous_system_number', '')
    isp = data.get('report', {}).get('full', {}).get('traits', {}).get('isp', '')

    description = f"Country: {c}, ASN: {asn}, ISP: {isp} "
    return {"description": description}

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

    # Normalize the score out of 100	
    if 'combined_score' in data['report']['full']:	
      threat_score = data['report']['full']['combined_score']	
    else:	
      if(indicator['indicator_types'][0] == 'benign'):	
        return {"threat_score": BENIGN_SCORE_MIN}	
      elif(indicator['indicator_types'][0] == 'unknown'):	
        return {"threat_score": UNKNOWN_SCORE_MIN}	
      if(indicator['indicator_types'][0] == 'anomalous-activity'):	
        return {"threat_score": SUSPICIOUS_SCORE_MIN}	
      if(indicator['indicator_types'][0] == 'malicious-activity'):	
        return {"threat_score": MALICIOUS_SCORE_MIN}	

    if threat_score > 10:	
      TOTAL = threat_score	
    else:	
      TOTAL = 10	
    threat_feed_ranges = [(0,1), (2,6), (7, TOTAL)]	

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


  def create_indicator_object(self, *properties):
    indicator_object = {}
    for prop in properties:
      if prop is not None:
        for key, value in prop.items():
          indicator_object[key] = value
    return indicator_object


  def get_threat_report(self, data):
    return {'x_ibm_original_threat_feed_data': data['report']}


  def add_fields_to_data(self, data):
    full_object = data['report'].get('full', {}) 

    if full_object:
      country_en_name = full_object.get('country', {}).get('names', {}).get('en', None)
      continent_en_name = full_object.get('continent', {}).get('names', {}).get('en', None)
      city_en_name = full_object.get('city', {}).get('names', {}).get('en', None)
      postal_code = full_object.get('postal', {}).get('code', None)

      country_obj = full_object.get('country', {})
      continent_obj = full_object.get('continent', {})
      city_obj = full_object.get('city', {})
      postal_obj = full_object.get('postal', {})
      if(postal_obj == {}): 
        full_object['postal'] = postal_obj

      country_obj['name'] = country_en_name
      continent_obj['name'] = continent_en_name
      city_obj['name'] = city_en_name
      postal_obj['code'] = postal_code

    try:  
      data['report']['full'] = full_object
    except:
      pass

    return data

  def get_threat_attributes(self, data):
    threat_attribute_report = []
    if 'report' in data:
      full_report = data['report'].get('full', {})
      # We pass the fields we want as attributes, with then new names of the fields
      country_fields = {
        'iso_code': 'Country Iso Code', 
        'name': 'Country Name', 
      }
      continent_fields = { 'code': 'Continent Code' }
      city_fields = {
        'name': 'City Name' 
      }
      location_fields = {
        'latitude': 'Latitude',
        'longitude': 'Longitude'
      }
      postal_fields = { 'code': 'Postal Code' }
      subdivisions_fields = { 'iso_code': 'Subdivisions Iso Code'}
      field_dict = {
        'continent': continent_fields, 
        'country': country_fields,
        'city': city_fields,
        'location': location_fields, 
        'postal': postal_fields, 
        'subdivisions': subdivisions_fields
      }
      for attribute_keys, attribute_value in field_dict.items():
        if full_report.get(attribute_keys):
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])
      if full_report.get('subdivisions') and isinstance(full_report['subdivisions'], list):
        threat_attribute_report.extend(self.get_subdivisions(full_report['subdivisions']))


    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def get_subdivisions(self, subdivisions_list: list) -> list:
      threat_attribute_report = []

      for subdivision in subdivisions_list:
        subdivision_dict = {
          'attribute_name': 'Subdivisions ISO Code',
          'attribute_value': subdivision['iso_code'],
          'attribute_type': evaluate_attribute_type(subdivision['iso_code'])
        }

      threat_attribute_report.append(subdivision_dict)

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

    CONNECTOR_NAME = "MaxMind_Connector"
    data_source['id'] = "MaxMind_Connector"
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

    # report = self.get_threat_report(json_data)
    # Add fields to json_report
    json_data = self.add_fields_to_data(json_data)

    pattern = self.get_pattern_from_json(json_data)
    external_reference = self.get_external_reference_from_json(json_data)
    indicator_types = self.get_indicator_types(json_data) #get indicator types from the report
    description = self.get_description(json_data) #get description from the report
    threat_score = self.get_threat_score(json_data, indicator_types)
    threat_attributes = self.get_threat_attributes(json_data)
    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)

    full_report = deepcopy(json_data)
    full_report['report']['full'] = [full_report['report']['full']]
    
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
    report = self.get_threat_report(full_report)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attributes):
      top_indicator.append(threat_attributes)

    indicator_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_object


    return stix_bundle
