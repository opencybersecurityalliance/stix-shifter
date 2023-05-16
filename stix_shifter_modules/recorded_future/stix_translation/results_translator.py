from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from . import sdo_translator
from os import path
# from stix_shifter_utils.normalization.normalization_helper import create_attributes
import json
import jmespath
from stix_shifter_utils.normalization.BaseNormalization import BaseNormalization
from ipaddress import ip_network, IPv4Network, IPv6Network
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
    c = value.get('report', {}).get('full', {}).get('data', {}).get('risk', {}).get('criticality', 1)
    if c == 0: indicator_type = 'benign'
    elif c == 1: indicator_type = 'unknown'
    elif c == 2: indicator_type = 'anomalous-activity'
    elif c >= 3: indicator_type = 'malicious-activity'
    return {'indicator_types':[indicator_type]}

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

    elif pattern_type == 'domain':
      pattern = "["+ pattern_type + "-name:value='" + value + "']"
  
    # Get ipv4 or ipv6
    elif pattern_type == 'ip':
      pattern = "["+ self.get_ip_address(value) + "-addr:value='" + value + "']"

    # Get Hash of type SHA-256, SHA-1, or MD5
    elif pattern_type == 'hash':
      pattern = "["+ self.find_hash_type_by_length(value) + "='" + value + "']"

    return pattern


  def get_description(self, data):
    value = "N/A"
    if data['report']['full'].get('data'):
      rf_score = data['report']['full']['data']['risk']['score']
      value = f"Score: {rf_score}/100"

    return {"description": value}

  def get_malware_object(self, data): 
    malware = []

    name = ""
    entitiesList = data['report']['relatedEntities']
    for entities in entitiesList:
      for entity in entities['entities']:
        if entity['entity']['type'] == 'MalwareCategory':
          name = entity['entity']['name']
          break
      if name != "":
        break  
    
    malware_info = {}
    malware_info['description'] = name
    malware_type = name
    if malware_type:
      malware_info['malware_types'] = malware_type
      malware.append (malware_info)    
    return malware

  def get_external_references(self, data):
    value = {
      "source_name": "RecordedFuture_Connector",
      "url": "N/A"
    }
    try:
      url = data['report']['full']['data']['intelCard']
      value['url'] = url
    except:
      pass         

    return {'external_references':[value]}

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

    range_min = 0
    range_max = 100

    if(indicator['indicator_types'][0] == 'benign'):
      if data['report']['full'].get('data') is None:
        return {"threat_score": BENIGN_SCORE_MIN}

      tis_range_min = BENIGN_SCORE_MIN
      tis_range_max = BENIGN_SCORE_MAX
      threat_score = data['report']['full']['data']['risk']['score']
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)

    elif indicator['indicator_types'][0] == 'unknown':
      if data['report']['full'].get('data') is None:
        return {"threat_score": UNKNOWN_SCORE_MIN}

      tis_range_min = UNKNOWN_SCORE_MIN
      tis_range_max = UNKNOWN_SCORE_MAX
      threat_score = data['report']['full']['data']['risk']['score']
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)

    elif (indicator['indicator_types'][0] == 'anomalous-activity'):
      if data['report']['full'].get('data') is None:
        return {"threat_score": SUSPICIOUS_SCORE_MIN}

      tis_range_min = SUSPICIOUS_SCORE_MIN
      tis_range_max = SUSPICIOUS_SCORE_MAX
      threat_score = data['report']['full']['data']['risk']['score']
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    else:
      if data['report']['full'].get('data') is None:
        return {"threat_score": UNKNOWN_SCORE_MIN}

      tis_range_min = MALICIOUS_SCORE_MIN
      tis_range_max = MALICIOUS_SCORE_MAX
      threat_score = data['report']['full']['data']['risk']['score']
      tis_score = tis_range_min + (tis_range_max-tis_range_min) * 1.0 * (threat_score-range_min) / (range_max - range_min)
    threat_score = {"threat_score": round(tis_score, 1)}
    return threat_score

  #
  # https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070646
  # Following method of populating malware object, it should have same attributes defined above STIX 2.1 malware spec.
  # e.g.  malwareObject={} malwareObject['malware_types'] = valueofMalwareType
  # Here its important to keep same key `malware_types`
  # returns list of malware objects or dict of malware object. 

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
            malwareNameList = jmespath.search("data.relatedEntities[?type=='RelatedMalwareCategory'].entities[].entity.name", full_report)
            if malwareNameList:
              for malwareName in malwareNameList: 
                malwareObject={}               
                malwareObject['malware_types'] = malwareName              
                malware_objects.append(malwareObject)
            relatedMalwareNameList = jmespath.search("data.relatedEntities[?type=='RelatedMalware'].entities[].entity.name", full_report)
            if relatedMalwareNameList:
              for malwareName in relatedMalwareNameList: 
                malwareObject={}               
                malwareObject['name'] = malwareName                              
                malware_objects.append(malwareObject)
            noteMalwareNameList = jmespath.search("data.analystNotes[].attributes.note_entities[?type=='Malware'].name", full_report)
            if noteMalwareNameList:
              for malwareNames in noteMalwareNameList: 
                for malwareName in malwareNames: 
                  malwareObject={}               
                  malwareObject['name'] = malwareName                              
                  malwareObject['malware_types'] = malwareName                              
                  malware_objects.append(malwareObject)                


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


  def get_threat_attributes(self, data):
    threat_attribute_report = []
    if 'report' in data:
      full_report = data['report'].get('full', {}).get('data', {})

      # We pass the fields we want as attributes, with then new names of the fields
      report_timestamps = full_report.get('timestamps', {})
      report_metrics = full_report.get('metrics', [])
      report_risk = full_report.get('risk', {})
      report_intel_card = {'intelCard': full_report.get('intelCard', {})}

      full_report = {
        'timestamps': report_timestamps, 
        'metrics': report_metrics, 
        'risk': report_risk, 
        'intelCard': report_intel_card
      }
      timestamps_fields = {
        'firstSeen': 'First Seen',
        'lastSeen': 'Last Seen'
      }
      intel_card_fields = { 'intelCard': 'Intel Card' }
      risk_fields = { 'riskSummary': 'Risk Summary' }

      metrics_fields = {
        'oneDayHits': 'One Day Hits',
        'totalHits': 'Total Hits',
        'sevenDaysHits': 'Seven Days Hits',
        'socialMediaHits': 'Social Media Hits',
        'undergroundForumHits': 'Underground Forum Hits',
        'infoSecHits': 'Info Sec Hits',
        'maliciousHits': 'Malicious Hits',
        'darkWebHits': 'Dark Web Hits',
        'pasteHits': 'Paste Hits',
        'technicalReportingHits': 'Technical Reporting Hits',
        'sixtyDaysHits': 'Sixty Days Hits',
      }

      # Use description instead?
      # "criticalityLabel": "Malicious",
      # "riskString": "3/14",
      # "rules": 3,
      # "criticality": 3,
      # "riskSummary": "3 of 14 Risk Rules currently observed.",
      # "score": 69,


      field_dict = {
        'timestamps': timestamps_fields, 
        'risk': risk_fields,
        'intelCard': intel_card_fields, 
      }

      for attribute_keys, attribute_value in field_dict.items():
        if attribute_keys in full_report:
          threat_attribute_report += create_attributes(attribute_value, full_report[attribute_keys])

      # Add metrics
      if report_metrics:
        metric_attributes = []
        for metric in report_metrics:
          for attribute_keys, attribute_value in metrics_fields.items():
            if attribute_keys in metric['type']:
              attribute_dict = {}
              attribute_dict['attribute_name'] = attribute_value
              attribute_dict['attribute_value'] = metric['value']
              attribute_dict['attribute_type'] = evaluate_attribute_type(metric['value'])            
              metric_attributes.append(attribute_dict)
        if metric_attributes:
          threat_attribute_report.extend(metric_attributes)

    return {'threat_attributes' : threat_attribute_report} if threat_attribute_report else None


  def get_threat_report(self, data):
    full_data = dict()
    success_result = False
    try:
      full_data = data['report']['full']
      success_result = data['report']['success']
    except:
      pass

    report = {'x_ibm_original_threat_feed_data': {'success': success_result, 'full': [full_data]}}
    return report

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
    CONNECTOR_NAME = "RecordedFuture_Connector"
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
    indicator_types = self.get_indicator_types(json_data) # obtain from report
    description = self.get_description(json_data) # obtain from report
    threat_score = self.get_threat_score(json_data, indicator_types)
    data_to_enrich_pattern = pattern['pattern']
    threat_attributes = self.get_threat_attributes(json_data)

    indicator_name = {'name': json_data['data']}
    indicator_object = self.create_indicator_object(pattern, external_reference, indicator_types, description, indicator_name)


    if json_data['report'].get('isIOCFound'): del json_data['report']['isIOCFound'] 


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

    extension_object = sdo_translator_object.create_extension_sdo(identity_object[0], NAMESPACE, nested_properties, toplevel_properties)
    stix_bundle['objects'] += extension_object

    # Add Indicator SDO
    identity_id = identity_object[0]['id']
    extension_id = extension_object[0]['id']
    report = self.get_threat_report(json_data)
    nested_indicator = []
    top_indicator = [threat_score, report]
    if (threat_attributes):
      top_indicator.append(threat_attributes)

    indicator_object = sdo_translator_object.create_indicator_sdo(indicator_object, identity_id, extension_id, nested_indicator, top_indicator)
    stix_bundle['objects'] += indicator_object


    # Add Malware SDO - Should return a list of malware dict
    data = json.dumps(json_data)
    data = "[" + data + "]"
    json_data = json.loads(data)
    malware_object = self.malware_from_report_attributes(json_data)

    if  malware_object:
      malware_stix_object = sdo_translator_object.create_malware_sdo(malware_object,indicator_object[0]['id'],data_to_enrich_pattern)
      stix_bundle['objects'] += malware_stix_object

    return stix_bundle
