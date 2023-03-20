""" test script to perform unit test case for okta translate results """
import unittest
from stix_shifter_modules.okta.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "okta"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "okta",
    "identity_class": "events"
}
options = {}

okta_sample_response = {
    "actor": {
        "id": "00u7rkrly9sNvp7sa5d7",
        "type": "User",
        "alternateId": "user1@login.com",
        "displayName": "user1",
        "detailEntry": None
    },
    "client": {
        "userAgent": {
            "rawUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "os": "Windows 10",
            "browser": "CHROME"
        },
        "zone": "None",
        "device": "Computer",
        "id": 'None',
        "ipAddress": "1.1.1.1",
        "geographicalContext": {
            "city": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "postalCode": "600006",
            "geolocation": {
                "lat": 12.8996,
                "lon": 80.2209
            }
        }
    },
    "device": None,
    "authenticationContext": {
        "authenticationProvider": "FACTOR_PROVIDER",
        "credentialProvider": "OKTA_CREDENTIAL_PROVIDER",
        "credentialType": None,
        "issuer": None,
        "interface": None,
        "authenticationStep": 0,
        "externalSessionId": "idxVwaF623uQNiVlG19PzFdDg"
    },
    "displayMessage": "Authentication of user via MFA",
    "eventType": "user.authentication.auth_via_mfa",
    "outcome": {
        "result": "FAILURE",
        "reason": "INVALID_CREDENTIALS"
    },
    "published": "2023-02-09T08:39:19.133Z",
    "securityContext": {
        "asNumber": 17488,
        "asOrg": "hathway cable and datacom limited",
        "isp": "hathway ip over cable internet",
        "domain": "hathway",
        "isProxy": False
    },
    "severity": "INFO",
    "debugContext": [{
        "debugData": {
            "authnRequestId": "Y-Sw7-z3z4tnCOyPQ4v3lwAADhQ",
            "pushOnlyResponseType": "OV_RESPONSE_APPROVE",
            "requestId": "Y-SxNlxdagytkKJV-Bs-AQAADGo",
            "requestUri": "/api/v1/authn/factors/opf7rkr4nsyDyTKnf5d7/transactions/ftqsm1uKG8ZsWaFgkE_m4cK"
                          "XMXQvK0TQ68/verify",
            "threatSuspected": "false",
            "factor": "OKTA_VERIFY_PUSH",
            "factorIntent": "AUTHENTICATION",
            "pushWithNumberChallengeResponseType": "OV_WITH_CHALLENGE_RESPONSE_ERROR",
            "url": "/api/v1/authn/factors/opf7rkr4nsyDyTKnf5d7/transactions/ftqsm1uKG8ZsWaFgkE_m4cKXMXQvK0TQ68/verify?"
        }
    }],
    "legacyEventType": "core.user.factor.attempt_fail",
    "transaction": {
        "type": "WEB",
        "id": "Y-SxNlxdagytkKJV-Bs-AQAADGo",
        "detail": {}
    },
    "uuid": "3e6c6109-a855-11ed-98eb-4781c6ece90f",
    "version": "0",
    "request": {
        "ipChain": [
            {
                "ip": ["2.2.2.2"]
            }
        ]
    },
    "target": [
        {
            "id": "00u7rkrly9sNvp7sa5d7",
            "type": "User",
            "alternateId": "user1@login.com",
            "displayName": "user1",
            "detailEntry": None
        },
        {
            "id": "pfd7rkr4nqHLoMqI85d7",
            "type": "AuthenticatorEnrollment",
            "alternateId": "unknown",
            "displayName": "Okta Verify",
            "detailEntry": {
                "methodTypeUsed": "Get a push notification"
            }
        }
    ]
}


class TestOktaResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for okta translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestOktaResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """
        to test ipv4-addr stix object properties
        """
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        ipv4_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        assert (ipv4_obj is not None), 'ipv4 object type not found'
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '1.1.1.1'

    def test_autonomous_system_and_domain_json_to_stix(self):
        """
        to test autonomous-system and domain stix object properties
        """
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        autonomous_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'autonomous-system')
        assert (autonomous_obj.keys() == {'type', 'number', 'name', 'x_isp', 'x_domain_ref'})
        assert (autonomous_obj is not None), 'autonomous system object type not found'
        assert autonomous_obj['type'] == 'autonomous-system'
        assert autonomous_obj['number'] == 17488

        domain_ref = autonomous_obj['x_domain_ref']
        assert (domain_ref in objects), f"domain_ref with key {autonomous_obj['x_domain_ref']} " \
                                        f"not found"
        domain_obj = objects[domain_ref]
        assert domain_obj['value'] == 'hathway'

    def test_user_account_json_to_stix(self):
        """to test user-account stix object properties"""
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        user_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert (user_obj is not None), 'user account object type not found'
        assert user_obj['type'] == 'user-account'
        assert user_obj['display_name'] == 'user1'
        assert user_obj['account_login'] == 'user1@login.com'
        assert user_obj['user_id'] == '00u7rkrly9sNvp7sa5d7'

    def test_x_okta_target_json_to_stix(self):
        """to test x-okta-target object properties"""

        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)

        client_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        target_refs = client_obj['x_target_refs']
        assert (all(
            target in objects for target in target_refs)), \
            f"one of the target object among {client_obj['x_target_refs']} is not found"
        target_obj = objects[target_refs[1]]
        assert (target_obj is not None), 'target object type not found'
        assert (target_obj.keys() == {'type', 'target_id', 'target_type', 'alternate_id', 'display_name',
                                      'detail_entry'})
        assert target_obj['type'] == 'x-okta-target'
        assert target_obj['target_id'] == 'pfd7rkr4nqHLoMqI85d7'
        assert target_obj['target_type'] == 'AuthenticatorEnrollment'
        assert target_obj['display_name'] == 'Okta Verify'
        assert target_obj['detail_entry'] == {
            "methodTypeUsed": "Get a push notification"
        }

    def test_software_json_to_stix(self):
        """to test software stix object properties"""
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        software_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'software')
        assert (software_obj is not None), 'software object type not found'
        assert software_obj['type'] == 'software'
        assert software_obj['name'] == 'CHROME'
        assert software_obj['x_client_os'] == 'Windows 10'
        assert software_obj['x_raw_user_agent'] \
               == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/108.0.0.0 Safari/537.36'

    def test_x_okta_client_json_to_stix(self):
        """to test x-okta-client object properties"""

        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        client_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-okta-client')

        assert (client_obj is not None), 'client object type not found'
        assert (client_obj.keys() == {'type', 'software_ref', 'network_zone_name', 'device', 'client_id', 'ip_ref',
                                      'geolocation_city', 'geolocation_state', 'geolocation_country',
                                      'geolocation_postalcode', 'geolocation_coordinates', 'autonomous_system_ref'})

        assert (all(
            index in objects for ref, index in client_obj.items() if '_ref' in ref)), \
            "one of the references in client object is not found"
        assert client_obj['type'] == 'x-okta-client'
        assert client_obj['device'] == 'Computer'
        assert client_obj['geolocation_country'] == 'India'
        assert client_obj['geolocation_coordinates'] == {'lat': 12.8996, 'lon': 80.2209}

    def test_x_okta_authentication_context_json_to_stix(self):
        """to test x-okta-authentication-context object properties"""

        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        authentication_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-okta-authentication-context')

        assert authentication_obj is not None
        assert authentication_obj['type'] == 'x-okta-authentication-context'
        assert authentication_obj['authentication_provider'] == 'FACTOR_PROVIDER'
        assert authentication_obj['credential_provider'] == 'OKTA_CREDENTIAL_PROVIDER'
        assert authentication_obj['session_id'] == 'idxVwaF623uQNiVlG19PzFdDg'

    def test_x_oca_event_json_to_stix(self):
        """to test x-oca-event object properties"""
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        event_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert (event_obj is not None), 'event object is not found'
        assert event_obj['type'] == 'x-oca-event'
        assert (event_obj.keys() == {'type', 'x_actor_ref', 'x_client_ref', 'ip_refs', 'x_authentication_context_ref',
                                     'x_event_description', 'action', 'outcome', 'x_outcome_reason',
                                     'x_severity', 'x_debug_ref', 'x_legacy_event_type', 'category',
                                     'x_transaction_id', 'x_event_unique_id', 'x_target_refs'})
        assert event_obj['x_severity'] == 'INFO'
        assert event_obj['action'] == 'user.authentication.auth_via_mfa'
        assert event_obj['outcome'] == 'FAILURE'
        assert event_obj['category'] == ['WEB']
        assert (all(ip_ref in objects for ip_ref in event_obj['ip_refs'])), "ip object is not found"
        assert (all(
            index in objects for ref, index in event_obj.items() if '_ref' in ref and not isinstance(index, list))), \
            "one of the references in client object is not found"
        assert (all(target in objects for ref, value in event_obj.items()
                    if 'x_target_refs' == ref for target in value)), "target object is not found"
        assert event_obj['x_outcome_reason'] == 'INVALID_CREDENTIALS'
        assert event_obj['x_event_unique_id'] == '3e6c6109-a855-11ed-98eb-4781c6ece90f'

    def test_debug_context_json_to_stix(self):
        """to test debug-context object properties"""
        objects = TestOktaResultsToStix.get_observed_data_objects(okta_sample_response)
        debug_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-okta-debug-context')
        event_obj = TestOktaResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert (debug_obj is not None), 'debug context object is not found'
        assert debug_obj['type'] == 'x-okta-debug-context'
        assert debug_obj['debug_data'] == {'authnRequestId': 'Y-Sw7-z3z4tnCOyPQ4v3lwAADhQ',
                                           'pushOnlyResponseType': 'OV_RESPONSE_APPROVE',
                                           'requestId': 'Y-SxNlxdagytkKJV-Bs-AQAADGo',
                                           'requestUri': '/api/v1/authn/factors/opf7rkr4nsyDyTKnf5d7/transactions'
                                                         '/ftqsm1uKG8ZsWaFgkE_m4cKXMXQvK0TQ68/verify',
                                           'threatSuspected': 'false', 'factor': 'OKTA_VERIFY_PUSH',
                                           'factorIntent': 'AUTHENTICATION',
                                           'pushWithNumberChallengeResponseType': 'OV_WITH_CHALLENGE_RESPONSE_ERROR',
                                           'url': '/api/v1/authn/factors/opf7rkr4nsyDyTKnf5d7/transactions/'
                                                  'ftqsm1uKG8ZsWaFgkE_m4cKXMXQvK0TQ68/verify?'}
        assert 'x_debug_ref' in event_obj.keys()
