""" test script to perform unit test case for cisco_secure_email translate results """
import unittest
from stix_shifter_modules.cisco_secure_email.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "cisco_secure_email"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "cisco_secure_email",
    "identity_class": "events"
}
options = {}

cisco_secure_email_sample_response = [
    {
        "attributes": {
            "hostName": "",
            "friendly_from": [
                "testuser123@email.com"
            ],
            "isCompleteData": "N/A",
            "messageStatus": {
                "1637": "Delivered"
            },
            "recipientMap": {
                "1637": [
                    "testuser13@email.com"
                ]
            },
            "senderIp": "11.111.11.11",
            "mailPolicy": [
                "DEFAULT"
            ],
            "senderGroup": "UNKNOWNLIST",
            "morInfo": {
                "midVsState": {
                    "1637": "Delivered"
                }
            },
            "subject": "Test ReplyTo message",
            "mid": [
                1637
            ],
            "senderDomain": "amazonses.com",
            "finalSubject": {
                "1637": "Test ReplyTo message"
            },
            "direction": "incoming",
            "icid": 1418,
            "morDetails": {},
            "replyTo": "testuser123@email.com",
            "timestamp": "04 Aug 2023 12:11:41 (GMT +00:00)",
            "messageID": {
                "1637": "<01000189c075eb9f-5fc5923c-5c03-4d1b-ad00-f75cc2c28fbf-000000@email.amazonses.com>"
            },
            "verdictChart": {
                "1637": "01141210"
            },
            "recipient": [
                "testuser13@email.com"
            ],
            "sender": "01000189c075eb9f-5fc5923c-5c03-4d1b-ad00-f75cc2c28fbf-000000@amazonses.com",
            "serialNumber": "EC2CD1D95C273722A23A-CA0C47E74D1B",
            "allIcid": [
                1418
            ],
            "sbrs": "3.4"
        }
    }
]


class TestCiscoSecureEmailResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for cisco_secure_email translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """ return the obj in the itr if constraint is true """
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        """ check whether the object belongs to respective stix object """
        return TestCiscoSecureEmailResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """test ipv4-addr stix object properties"""
        objects = TestCiscoSecureEmailResultsToStix.get_observed_data_objects(cisco_secure_email_sample_response)
        ipv4_obj = TestCiscoSecureEmailResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        assert ipv4_obj is not None
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '11.111.11.11'

    def test_email_addr_json_to_stix(self):
        """test email-addr stix object properties"""
        objects = TestCiscoSecureEmailResultsToStix.get_observed_data_objects(cisco_secure_email_sample_response)
        email_obj = TestCiscoSecureEmailResultsToStix.get_first_of_type(objects.values(), 'email-addr')
        assert email_obj is not None
        assert email_obj['type'] == 'email-addr'
        assert email_obj['value'] == 'testuser123@email.com'

    def test_email_message_json_to_stix(self):
        """test email-message stix object properties"""
        objects = TestCiscoSecureEmailResultsToStix.get_observed_data_objects(cisco_secure_email_sample_response)
        email_msg_obj = TestCiscoSecureEmailResultsToStix.get_first_of_type(objects.values(), 'email-message')
        assert email_msg_obj is not None
        assert (email_msg_obj.keys() == {'type', 'from_ref', 'is_multipart', 'x_sender_group', 'subject',
                                         'x_cisco_mid', 'x_cisco_icid', 'date', 'x_message_id_header', 'to_refs',
                                         'sender_ref', 'x_serial_number'})
        assert email_msg_obj['type'] == 'email-message'
        assert email_msg_obj['from_ref'] == '0'
        assert email_msg_obj['is_multipart'] == True
        assert email_msg_obj['subject'] == 'Test ReplyTo message'

    def test_cisco_email_msgevent_json_to_stix(self):
        """test x-cisco-email-msgevent stix object properties"""
        objects = TestCiscoSecureEmailResultsToStix.get_observed_data_objects(cisco_secure_email_sample_response)
        cisco_email_obj = TestCiscoSecureEmailResultsToStix.get_first_of_type(objects.values(),
                                                                              'x-cisco-email-msgevent')
        assert cisco_email_obj is not None
        assert (cisco_email_obj.keys() == {'type', 'message_status', 'mail_policy', 'direction', 'reply_to',
                                           'sbrs_score'})
        assert cisco_email_obj['type'] == 'x-cisco-email-msgevent'
        assert cisco_email_obj['message_status'] == 'Delivered'
        assert cisco_email_obj['mail_policy'] == ['DEFAULT']
        assert cisco_email_obj['direction'] == 'incoming'


    def test_domain_name_json_to_stix(self):
        """test domain-name stix object properties"""
        objects = TestCiscoSecureEmailResultsToStix.get_observed_data_objects(cisco_secure_email_sample_response)
        domain_obj = TestCiscoSecureEmailResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert domain_obj is not None
        assert (domain_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == 'amazonses.com'
        assert domain_obj['resolves_to_refs'] == ['3']
