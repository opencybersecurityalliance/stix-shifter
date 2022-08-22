from ipaddress import ip_network, IPv4Network, IPv6Network
from urllib.parse import urlparse

def create_attributes(attribute_fields, data):
  ''' Used to create a custom property of type array of objects to add on a STIX 2.1 SDO
  :param attribute_fields: is a dict object with keys being property fields in the data object that we are combing through
          the value pair of the dict object is the new name of th attribute field
  :type attribute_fields: dict
  :param data: a json object that we are going to comb through to create attribute custom_property
  :type data: dict
  :return: list of dict attributes
  :return type: list

  an example:

  attribute_fields = {'malicious_file': 'Malware'}
  
  data = {
    'benign': False, 
    'malicious_file': '12345_hash_value'
  }

  Return output:

  "attributes": [
    "attribute_name": "Malware",
    "attribute_value": "12345_hash_value",
    "attribute_type": "string"
  ]
  '''
  attribute_report = []
  for attribute, value in attribute_fields.items():
    if attribute in data:
      attribute_dict = {}
      attribute_dict['attribute_name'] = value
      attribute_dict['attribute_value'] = data[attribute]
      attribute_dict['attribute_type'] = evaluate_attribute_type(data[attribute])
      attribute_report.append(attribute_dict) if attribute_dict['attribute_type'] is not None else ''
  return attribute_report


def evaluate_attribute_type(attribute):
  '''
  :param attribute: could be any type
  :return: number if attribute is int, float or complex
  :return: string if it is a string
  :return: ip if it is a string which is an ipaddress
  :return: URI if it is a URL
  :return: lat_lng if it is a latitude or longitude coordinates
  '''
  attribute_type = None
  if isinstance(attribute, (int, float, complex)):
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
  # Check if string is a URI string
  result = urlparse(x)
  return all([result.scheme, result.netloc])
