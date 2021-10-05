import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.proofpoint.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
import json
from stix_shifter.stix_translation import stix_translation

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

event_data=[{
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
        }]
class TestProofpointResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for proofpoint translate results
    """

    def test_custom_mapping(self):
        # data_source_string = json.dumps(data_source)
        # data_string = json.dumps(message_data)
        # translation = stix_translation.StixTranslation()
        # result_bundle = translation.translate('proofpoint', 'results', data_source_string, data_string, options)

        result_bundle = entry_point.translate_results(json.dumps(data_source), json.dumps([event_data]))

        print('result_bundle :', result_bundle)