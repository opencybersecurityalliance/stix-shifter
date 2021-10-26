import unittest
from stix_shifter_modules.proofpoint.entry_point import EntryPoint
import json
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()

MODULE = "proofpoint"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Proofpoint",
    "identity_class": "events"
}
options = {}

event_data={
            "is_multipart": True,
            "GUID": "Ggfsdfsdf",

            "Header": {
                "ccAddresses": [],
                "fromAddress": [
                    "Header@xxx.com"
                ],
                "headerFrom": "\"j.\" <headerFrom@xxx.com>",
                "headerReplyTo": None,
                "replyToAddress": [],
                "toAddresses": [],
                "xmailer": None
            },
            "cluster": "hosted",
            "completelyRewritten": True,
            "id": "1828003vsdv05566e842",
            "impostorScore": 0,
            "malwareScore": 0,
            "messageID": "<SI2PR0dfbvd.xxxx@xxx.com.com>",
            "messageParts": [
                {
                    "contentType": "text/html",
                    "disposition": "inline",
                    "filename": "text.html",
                    "md5": "fcfa9b21f43fbdf02965263c63e",
                    "oContentType": "text/html",
                    "sandboxStatus": "None",
                    "sha256": "72d3dc7a01dfbdbe8e871536864f56bf235ba08ff259105ac"
                },
{
                    "contentType": "text/html",
                    "disposition": "inline",
                    "filename": "text2.html",
                    "md5": "fcfa9b21f43fbdf02965263c63e",
                    "oContentType": "text/html",
                    "sandboxStatus": None,
                    "sha256": "72d3dc7a01dfbdbe8e871536864f56bf235ba08ff259105bd"
                }
            ],
            "messageSize": 10171,
            "messageTime": "2021-06-02T13:41:32.000Z",
            "modulesRun": [
                "av",
                "spf",
                "dkimv",
                "spam",
                "dmarc",
                "urldefense"
            ],
            "phishScore": 0,
            "policyRoutes": [
                "default_inbound",
                "allow_relay"
            ],
            "quarantineFolder": None,
            "quarantineRule": None,
            "recipient": [
                "recipient@xxx.com"
            ],
            "sender": "sender@xxx.com",
            "senderIP": "400.000.000",
            "spamScore": 43,
            "subject": "=",
            "threatsInfoMap": [
                {
                    "campaignID": None,
                    "classification": "phish",
                    "threat": "https://bit.ly",
                    "threatID": "45fe3b35ghkk2b8916934b6c0a536cc9b2603d03",
                    "threatStatus": "active",
                    "threatTime": "2021-06-03T07:17:11.000Z",
                    "threatType": "url",
                    "threatUrl": "https://threatinsight.proofpoint.com"
                },
{
                    "campaignID": None,
                    "classification": "phish",
                    "threat": "https://bit123.ly",
                    "threatID": "45fe3b35ghkk2b8916934b6c0a536cc9b2603d04",
                    "threatStatus": "active",
                    "threatTime": "2021-06-04T07:17:11.000Z",
                    "threatType": "url",
                    "threatUrl": "https://threatinsight.proofpoint.com"
                }
            ]
        }

def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestProofpointResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for proofpoint translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestProofpointResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)


    def test_common_mapping(self):
        result_bundle = entry_point.translate_results(json.dumps(data_source), json.dumps(event_data))
        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert (result_bundle_identity['type'] == data_source['type'])
        assert (result_bundle_identity['id'] == data_source['id'])
        assert (result_bundle_identity['name'] == data_source['name'])
        assert (result_bundle_identity['identity_class']
                == data_source['identity_class'])

        observed_data = result_bundle_objects[1]

        assert (observed_data['id'] is not None)
        assert (observed_data['type'] == "observed-data")
        assert (observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert (observed_data['number_observed'] == 1)
        assert (observed_data['created'] is not None)
        assert (observed_data['modified'] is not None)
        assert (observed_data['first_observed'] is not None)
        assert (observed_data['last_observed'] is not None)

    def test_custom_mapping(self):
        result_bundle = entry_point.translate_results(json.dumps(data_source), json.dumps([event_data]))
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert ('objects' in observed_data)
        objects = observed_data['objects']
        curr_obj = TestProofpointResultsToStix.get_first_of_type(objects.values(), 'email-message')
        assert (curr_obj is not None), 'email-message object type not found'
        assert ("type" in curr_obj.keys())
        assert ("date" in curr_obj.keys())