from stix_shifter_utils.modules.base.stix_transmission.base_results_connector import BaseResultsConnector
from stix_shifter_utils.utils.error_response import ErrorResponder
from stix_shifter_utils.utils import logger
import json
from httplib2 import ServerNotFoundError
from google.auth.exceptions import RefreshError
import copy
import re


class ResultsConnector(BaseResultsConnector):
    EMAIL_PATTERN = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)
        self.connector = __name__.split('.')[1]

    def create_results_connection(self, search_id, offset, length):
        """
        Fetching the results using search id, offset and length
        :param search_id: str, search id generated in transmit query
        :param offset: str, offset value
        :param length: str, length value
        :return: dict
        """
        return_obj = {}
        response_dict = {}
        result = []
        next_page_token = '0'
        result_count = 0
        page_size = self.api_client.result_limit

        try:
            response_wrapper = self.api_client.get_search_results(search_id, next_page_token, page_size)
            response_text = json.loads(response_wrapper[1])
            if response_wrapper[0].status == 200:
                if 'detections' in response_text.keys():
                    result_count += len(response_text['detections'])
                    result.append(response_text['detections'])
                    # make api call again, if there is next page token in the response and results fetched is less than
                    # the result limit of the connector.
                    while 'nextPageToken' in response_text.keys():
                        if result_count < self.api_client.result_limit:
                            page_size = self.api_client.result_limit - result_count
                            next_response = self.api_client.get_search_results(search_id,
                                                                               response_text['nextPageToken'],
                                                                               page_size)
                            response_text = json.loads(next_response[1])
                            if next_response[0].status == 200:
                                if 'detections' in response_text.keys():
                                    result_count += len(response_text['detections'])
                                    result.append(response_text['detections'])
                            else:
                                response_dict['code'] = next_response[0].status
                                response_dict['message'] = response_text['error'].get('message')
                                ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                                          connector=self.connector)
                                return_obj = self.invalid_response(return_obj, response_dict,
                                                                   next_response[0].status, response_text)
                                break
                        else:
                            break
                return_obj['success'] = True
                if result:
                    final_result = ResultsConnector.get_results_data(result)
                    return_obj['data'] = final_result[int(offset):(int(offset) + int(length))] if final_result else []
                else:
                    return_obj['data'] = []
                # delete the error details if partial results are fetched
                if 'code' in return_obj and 'error' in return_obj and return_obj['data']:
                    del return_obj['code']
                    del return_obj['error']
            else:
                return_obj = self.invalid_response(return_obj, response_dict, response_wrapper[0].status,
                                                   response_text)

        except ServerNotFoundError:
            response_dict['code'] = 1010
            response_dict['message'] = "Invalid Host"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except RefreshError:
            response_dict['code'] = 1015
            response_dict['message'] = "Invalid Client Email"
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except ValueError as r_ex:
            if 'Could not deserialize key data' in str(r_ex):
                response_dict['message'] = r_ex
                response_dict['code'] = 1015
            else:
                response_dict['message'] = f'cannot parse {r_ex}'
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        except Exception as exp:
            if "timed out" in str(exp):
                response_dict['code'] = 120
                response_dict['message'] = str(exp)
            else:
                response_dict['message'] = exp
            self.logger.error('error when getting search results: %s', exp)
            ErrorResponder.fill_error(return_obj, response_dict, ['message'], connector=self.connector)

        finally:
            if 'code' in response_dict:
                if response_dict['code'] not in (1010, 1015):
                    self.api_client.delete_search(search_id)
            else:
                self.api_client.delete_search(search_id)

        return return_obj

    def invalid_response(self, return_obj, response_dict, status, response_text):
        """
        handle error response
        :return dict
        """
        response_dict['code'] = status
        response_dict['message'] = response_text['error'].get('message')
        ErrorResponder.fill_error(return_obj, response_dict, ['message'],
                                  connector=self.connector)
        return return_obj

    @staticmethod
    def get_results_data(response_text):

        """
        Format the input results
        :return list
        """
        final_result = []

        for log in response_text:
            if isinstance(log, list):
                for element in log:
                    result_dict = ResultsConnector.get_logs(element)
                    final_result.append(result_dict)
            else:
                result_dict = ResultsConnector.get_logs(log)
                final_result.append(result_dict)
        return final_result

    @staticmethod
    def get_logs(element):
        """
        Formats the input with detection and collectionElements
        :return dict
        """
        result_dict = {}
        event = element['collectionElements'][0]['references'][0]
        formatted_event = ResultsConnector.format_event_data(event)
        detection = {"detection": element['detection'][0]}
        result_dict.update(formatted_event)
        result_dict.update(detection)
        return result_dict

    @staticmethod
    def format_event_data(events):
        """
        formats the results data
        :return dict
        """
        for noun in ('principal', 'src', 'target'):
            if noun in events['event'].keys():
                events = ResultsConnector.format_registry_result(events, noun)
                events = ResultsConnector.format_software_result(events, noun)
                events = ResultsConnector.format_user_account(events, noun)
        events = ResultsConnector.validate_guardduty_event(events)
        if 'network' in events['event'].keys():
            events = ResultsConnector.format_network_event(events)
        if 'securityResult' in events['event'].keys():
            events = ResultsConnector.format_security_result(events)

        return events

    @staticmethod
    def format_user_account(events, noun):
        """
        formats user account object
        :param events: dict
        :param noun: str
        :return: dict
        """
        if 'user' in events['event'][noun].keys():
            if 'userid' not in events['event'][noun]['user'].keys():
                if 'userDisplayName' in events['event'][noun]['user'] or \
                        'accountType' in events['event'][noun]['user'] or \
                        'windowsSid' in events['event'][noun]['user']:
                    events['event'][noun]['user'].update({'userid': 'UNAVAILABLE'})
            if 'emailAddresses' in events['event'][noun]['user'].keys():
                new_obj_list = []
                for email_list in events['event'][noun]['user']['emailAddresses']:
                    email = email_list.split(":")
                    for em in email:
                        if ResultsConnector.EMAIL_PATTERN.match(str(em)):
                            new_obj_list.append(em)
                if new_obj_list:
                    events['event'][noun]['user']['emailAddresses'] = new_obj_list
                else:
                    del events['event'][noun]['user']['emailAddresses']
        return events

    @staticmethod
    def format_security_result(events):
        """
        format the security result data
        :param events: dict
        :return: dict
        """
        for result in range(len(events['event']['securityResult'])):

            if 'severity' in events['event']['securityResult'][result].keys():
                events['event']['securityResult'][result]['severity'] = \
                    ResultsConnector.format_severity_result(
                        events['event']['securityResult'][result]['severity'])

            if 'category' in events['event']['securityResult'][result].keys():
                events['event']['securityResult'][result]['category'] = \
                    ResultsConnector.format_category_result(
                        events['event']['securityResult'][result]['category'][0])
            else:
                events['event']['securityResult'][result]['category'] = 'alert'

        return events

    @staticmethod
    def format_severity_result(severity):
        """
        convert the gcp chronicle severity value to stix value
        :param severity: str
        :return: int
        """
        if severity == "INFORMATIONAL":
            severity = 16
        if severity == "ERROR":
            severity = 32
        elif severity == "LOW":
            severity = 48
        elif severity == "MEDIUM":
            severity = 64
        elif severity == "HIGH":
            severity = 80
        elif severity == "CRITICAL":
            severity = 100
        else:
            severity = 16

        return severity

    @staticmethod
    def format_category_result(category):
        """
        convert gcp chronicle category value to stix value
        :param category: str
        :return: str
        """
        if category in ["SOFTWARE_SUSPICIOUS", "NETWORK_SUSPICIOUS", "NETWORK_CATEGORIZED_CONTENT",
                        "NETWORK_DENIAL_OF_SERVICE", "NETWORK_RECON", "NETWORK_COMMAND_AND_CONTROL", "EXPLOIT",
                        "DATA_EXFILTRATION", "DATA_AT_REST", "DATA_DESTRUCTION"]:
            category = 'alert'
        elif category == "POLICY_VIOLATION":
            category = 'policy'
        elif category in ["ACL_VIOLATION", "AUTH_VIOLATION"]:
            category = 'violation'
        elif category in ["SOFTWARE_MALICIOUS", "SOFTWARE_PUA", "NETWORK_MALICIOUS", "MAIL_SPAM", "MAIL_PHISHING",
                          "MAIL_SPOOFING"]:
            category = 'threat'
        return category

    @staticmethod
    def format_registry_result(events, noun):
        """
        format the registry event
        :param events: dict
        :param noun: string
        :return: dict
        """
        # remove registry object if registry key is not present
        if 'registry' in events['event'][noun].keys():
            if 'registryKey' not in events['event'][noun]['registry'].keys() and \
                    'registryValueData' in events['event'][noun]['registry'].keys():
                del events['event'][noun]['registry']
            else:
                # format registry value data
                registry_value_dict = {}
                registry_build_data = copy.deepcopy(events['event'][noun]['registry'])
                events['event'][noun]['registry']['registryValues'] = []
                for key, value in registry_build_data.items():
                    if key in ('registryValueName', 'registryValueData'):
                        registry_value_dict.update({key: value})
                        events['event'][noun]['registry'].pop(key)
                events['event'][noun]['registry']['registryValues'].append(registry_value_dict)
        return events

    @staticmethod
    def format_software_result(events, noun):
        """
        format software data
        :param events: dict
        :param noun: string
        :return: dict
        """
        if 'asset' in events['event'][noun].keys():
            if 'platformSoftware' in events['event'][noun]['asset'].keys():
                if "platform" not in events['event'][noun]['asset']['platformSoftware'].keys():
                    events['event'][noun]['asset']['platformSoftware']['platform'] = 'UNKNOWN_PLATFORM'
            if 'software' in events['event'][noun]['asset'].keys():
                if "name" not in events['event'][noun]['asset']['software'].keys():
                    events['event'][noun]['asset']['software']['name'] = 'unknown'
        return events

    @staticmethod
    def validate_guardduty_event(events):
        """
        validate guardduty event
        :param events: dict
        :return: dict
        """
        # change the target location name to principal location name if resource role is target in AWS Guardduty
        if events.get('event', {}).get('metadata', {}).get('productName') == 'AWS GuardDuty' and \
                events.get('event', {}).get('additional', {}).get('resourceRole') == 'TARGET':
            if events.get('event', {}).get('target', {}).get('location', {}).get('name', "") != "":
                if 'principal' in events.get('event', {}) and 'location' in events['event'].get('principal', {}):
                    if events['event']['principal']['location'].get('name', "") == "":
                        events['event']['principal']['location']['name'] = events['event']['target']['location']['name']
                        del events['event']['target']['location']['name']

        return events

    @staticmethod
    def format_network_event(events):
        """
        format network data
        :param events: dict
        :return: dict
        """
        network_keys = events['event']['network'].keys()
        # set is_multipart with false as default if there is email message property
        if 'email' in network_keys:
            if 'subject' in events['event']['network']['email'].keys():
                events['event']['network']['email']['isMultipart'] = False
            # validate the email
            net_email_copy = copy.deepcopy(events['event']['network']['email'])
            for mail_id in ['to', 'cc', 'bcc']:
                new_obj_list = []
                if mail_id in net_email_copy:
                    for email_list in net_email_copy[mail_id]:
                        email = email_list.split(":")
                        for em in email:
                            if ResultsConnector.EMAIL_PATTERN.match(str(em)):
                                new_obj_list.append(em)
                    if new_obj_list:
                        events['event']['network']['email'][mail_id] = new_obj_list
                    else:
                        del events['event']['network']['email'][mail_id]

        # donot create network traffic object if there is no ip
        if not (events['event'].get('principal', {}).get('ip') or events['event'].get('src', {}).get('ip') or
                events['event'].get('target', {}).get('ip')):
            network_copy = copy.deepcopy(events['event']['network'])
            for proto in network_copy:
                if proto not in ('email', 'asn', 'dns_domain'):
                    del events['event']['network'][proto]
        else:
            # set the values for protocol if it is not present for a network event
            if 'applicationProtocol' not in network_keys and 'ipProtocol' not in network_keys:
                for udm_protocol in ['dns', 'dhcp', 'http', 'smtp', 'ftp', 'tls']:
                    if udm_protocol in network_keys:
                        events['event']['network']['applicationProtocol'] = udm_protocol
                if 'applicationProtocol' not in events['event']['network'].keys() \
                        and (set(events['event']['network'].keys()) - set(['email', 'asn', 'dns_domain'])):
                    events['event']['network']['ipProtocol'] = 'tcp'
        return events
