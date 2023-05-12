from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
import json
from ipaddress import ip_network, IPv4Network, IPv6Network
import uuid
from urllib.parse import urlparse
from stix_shifter_utils.utils import logger
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
  def get_indicator_types(self, data):
    indicator_type = 'unknown'
    verdict_list = list(findkeys(data, 'verdict'))
    if verdict_list:
      verdict = verdict_list[0]
      if verdict == 'Whitelisted':
        indicator_type = 'benign'

    if indicator_type == 'unknown':
      score_list = list(findkeys(data, 'combined_score'))
      if score_list:
        score = score_list[0]
        if score < 3:
          indicator_type = 'benign'
        elif score < 7:
          indicator_type = 'anomalous-activity'
        elif score >= 7:
          indicator_type = 'malicious-activity'
        else:
          indicator_type = 'unknown'
    return {'indicator_types': [indicator_type]}


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
    pulse_list = []
    pulse_count = 0
    try:
      pulse_count = data['report']['full']['pulse_info']['count']
      pulse_list = data['report']['full']['pulse_info']['pluses']
    except:
      pass

    malicious_count = 0
    for entry in pulse_list:
      taglist = entry.get('tags') if entry.get('tags') is not None else []
      for t in taglist:
        if t.lower() == 'malicious':
          malicious_count += 1

    description = f"Malicious Pulses: {str(malicious_count)}/{str(pulse_count)}"
    description_object = {'description': description}
    return description_object


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
    score_list = list(findkeys(data, 'combined_score'))
    if score_list:
      combined_score = score_list[0]
      threat_score = combined_score
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


  def sighting_from_report_attributes(self,data):
    try:
      sighting={}    
      pulse_count_list = list(findkeys(data, 'pulse_info'))
      if pulse_count_list:
        count = pulse_count_list[0]['count']
        sighting['count'] = int(count)
      else:
        sighting['count'] = 0
      return sighting
    except ValueError:
      raise ValueError("Exception occurred to parse report data for sighting SDO")           


  def retrieve_malware_object(self, src_malware_families, dst_objects):
    if isinstance(src_malware_families, list):
      for item in src_malware_families:
        malware_obj = {}
        malware_obj['name'] = item
        malware_obj['malware_type'] = 'unknown'
        is_existed = False
        for existed_obj in dst_objects:
          if existed_obj['name'] and malware_obj['name'].lower() == existed_obj['name'].lower():
            is_existed = True
            break
        if is_existed == False:
          dst_objects.append(malware_obj)


  def malware_from_report_attributes(self,data):
    try:
      malware_objects=[]            
      json_data = data[0]
      if 'report' in json_data:
        report = json_data['report']
        if 'full' in report:
          report_full = report['full']
          if not isinstance(report_full, list):
                report_full = [report_full]          
          for full_report in report_full:
            malwareObject={}

            detection_list = list(findkeys(full_report, 'detection'))
            if detection_list:
              detections = detection_list[0]
              for d in detections:
                mObj = {}
                mObj['name'] = d
                if 'Ransom' in d:
                  mObj['malware_types'] = 'ransomware'
                else:
                  mObj['malware_types'] = 'unknown'
                if (mObj not in malware_objects):
                  malware_objects.append(mObj)
            
            ids_detection_list = list(findkeys(full_report, 'ids_detections'))
            if ids_detection_list:
              ids_detections = ids_detection_list[0]
              for idsdetection in ids_detections:
                if 'category' in idsdetection and idsdetection['category'] is not None and idsdetection['category'].lower() == 'malware':
                  if 'malware_name' in idsdetection and idsdetection['malware_name'] != '':
                      malwareObject['name'] = idsdetection['malware_name']
                  if 'subcategory' in idsdetection and idsdetection['subcategory'] != '':
                    malwareObject['malware_types'] = idsdetection['subcategory']
                    if (malwareObject not in malware_objects):
                      malware_objects.append(malwareObject)

            alienvault_malware_families = []
            try:
              alienvault_malware_families = full_report['pulse_info']['related']['alienvault']['malware_families']
            except:
              pass
            self.retrieve_malware_object(alienvault_malware_families, malware_objects)
            
            other_malware_families = []
            try:
              other_malware_families = full_report['pulse_info']['related']['other']['malware_families']
            except:
              pass
            self.retrieve_malware_object(other_malware_families, malware_objects)

      return malware_objects
    except ValueError:
      raise ValueError("Exception occured to parse report data for malware SDO")   


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
    backup_combined_score = None

    try:
      backup_combined_score = full_object['analysis']['plugins']['cuckoo']['result']['info']['combined_score']
      full_object['analysis']['combined_score'] = backup_combined_score
    except:
      pass
    
    try:
      # Remove unnecessary parts from full report to reduce total size
      if full_object['analysis'].get('plugins', {}):
        del full_object['analysis']['plugins']
    except:
      pass

    data['report']['full'] = full_object

    return data


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    ids_detection_report = []    

    if 'report' in data:
      full_report = data['report'].get('full', {})
      ids_detection_report = full_report.get('ids_detections', [])
      # We pass the fields we want as attributes, with then new names of the fields

      if data['dataType'] == 'hash':
        analysis_results = full_report.get('analysis', {}).get('info', {})
        analysis_fields = {
          'md5': 'MD5', 
          'sha1': 'SHA-1',
          'sha256': 'SHA-256',
          'filesize': 'File Size',
          'file_type': 'File Type',
          'file_class': 'File Class'
        }
        field_dict = { 'results': analysis_fields, }

        full_report = analysis_results
        for attribute_keys, attribute_value in field_dict.items():
          if full_report.get(attribute_keys):
            threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      elif data['dataType'] == 'ip':
        full_fields = {
          'asn': 'ASN',
          'city': 'City',
          'country_name': 'Country Name',
          'latitude': 'Latitude',
          'longitude': 'Longitude'
        }
        
        field_dict = { 'full': full_fields, }

        full_report = data['report']
        for attribute_keys, attribute_value in field_dict.items():
          if attribute_keys in full_report:
            threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

        for threat in threat_attribute_report:
          if threat.get('attribute_name').lower() == 'latitude' or threat.get('attribute_name').lower() == 'longitude':
            threat['attribute_type'] = 'lat_lng'
      

      # We use the same logic to add IDS Detection attribute for hash/IP
      if ids_detection_report:
        id_string = ''
        for ids in ids_detection_report:
          if ids.get('name'):
            id_string += ids.get('name') + ', '
        if id_string:
          id_string = id_string[:-2] # Get rid of ', ' at the end
          ids_dict = {
            'attribute_name': 'IDS Detections',
            'attribute_value': id_string,
            'attribute_type': 'string'
          }
          threat_attribute_report.append(ids_dict)

    self.get_location(threat_attribute_report)

    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def get_location(self, threat_attributes):
    location_dict = {}
    remove_threat = []
    for threat in threat_attributes:
      if threat.get('attribute_name').lower() == 'latitude' or threat.get('attribute_name').lower() == 'longitude':
        if threat.get('attribute_name').lower() == 'latitude': location_dict['lat'] = threat['attribute_value']
        else: location_dict['lng'] = threat['attribute_value']
        remove_threat.append(threat)
    if location_dict:
      location_attribute = {
        'attribute_name': 'Location',
        'attribute_value': json.dumps(location_dict),
        'attribute_type': 'lat_lng'
      }
      threat_attributes.append(location_attribute)
      for threat in remove_threat:
        threat_attributes.remove(threat)


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

    CONNECTOR_NAME = "OTXQuery_Connector"
    data_source['id'] = CONNECTOR_NAME
    try:
      uuid.UUID(json_data["namespace"])
    except ValueError:
      raise ValueError("Namespace is not valid UUID")
    NAMESPACE = json_data["namespace"]
    data_source['name'] = CONNECTOR_NAME

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
    data_to_enrich_pattern = pattern['pattern']

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

    indicator_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_object

    # Add Malware SDO
    data = json.dumps(full_report)
    data = "[" + data + "]"
    full_report = json.loads(data)

    malware_object = self.malware_from_report_attributes(full_report)
    if  malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object,indicator_object[0]['id'],data_to_enrich_pattern)
      stix_bundle['objects'] += malware_stix_object

    #Sighting SDO
    sighting_object = self.sighting_from_report_attributes(full_report)
    if (len(sighting_object) > 0):
      sighting_stix_object = sdo_translator_object.create_sighting_sdo(sighting_object,indicator_object[0]['id'])
      stix_bundle['objects'] += sighting_stix_object

    return stix_bundle
