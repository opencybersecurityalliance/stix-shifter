from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.alienvault_otx.stix_transmission.api_client import prepare_response
from unittest.mock import patch
from collections import namedtuple
import unittest
from types import SimpleNamespace

MODULE_NAME = "mandiant"
namespace = "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"

SAMPLE_DATA = '{"data": "34.102.136.180", "dataType": "ip"}'

DATA = {"code": 200, "data": "34.102.136.180", "report": {"success": "True", "full": {"first_seen": "2020-06-02T23:00:11.000Z", "last_seen": "2022-08-04T08:02:21.000Z", "sources": [{"first_seen": "2020-08-14T23:34:01.314+0000", "last_seen": "2021-10-27T23:34:14.796+0000", "osint": "True", "category": ["exploit/vuln-scanning", "exploit"], "source_name": "blocklist_net_ua"}, {"first_seen": "2020-11-06T22:10:01.936+0000", "last_seen": "2022-05-21T00:10:00.709+0000", "osint": "True", "category": ["phishing", "malware"], "source_name": "phishstats"}, {"first_seen": "2021-02-13T22:05:01.791+0000", "last_seen": "2021-02-13T22:05:01.791+0000", "osint": "True", "category": [], "source_name": "stopforumspam"}, {"first_seen": "2020-07-23T18:02:13.939+0000", "last_seen": "2022-08-04T08:02:21.859+0000", "osint": "False", "category": [], "source_name": "Mandiant"}, {"first_seen": "2020-11-10T20:00:02.556+0000", "last_seen": "2020-11-28T20:00:03.098+0000", "osint": "True", "category": ["exploit/vuln-scanning", "exploit"], "source_name": "alienvault_reputation"}, {"first_seen": "2020-06-02T23:00:11.953+0000", "last_seen": "2022-01-02T23:07:04.922+0000", "osint": "True", "category": ["phishing"], "source_name": "phishtank"}], "mscore": 50, "verdict": {"mlVerdict": {"confidenceScore": 0.08254789664468065, "modelVersion": "7.0.0", "verdict": "benign", "reasoning": {"response_count": 7, "benign_count": 3, "neighbor_influence": "benign", "confidence_count": {"malicious": {"high": 0, "low": 3, "med": 1}, "benign": {"high": 2, "low": 1, "med": 0}}, "source_count": 112, "malicious_count": 4, "tp": {"tif": {"futex.re": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Futex.re", "malicious_count": 0}, "other": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Other", "malicious_count": 0}, "voipbl": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Voipbl", "malicious_count": 0}, "darklist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Darklist", "malicious_count": 0}, "greensnow": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Greensnow", "malicious_count": 0}, "dch": {"response_count": 1, "benign_count": 1, "source_count": 1, "confidence": "low", "name": "Dch", "malicious_count": 0}, "blocklist_net_ua": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Blocklist Net Ua", "malicious_count": 0}, "myip_blacklist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Myip Blacklist", "malicious_count": 0}, "turris_greylist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Turris Greylist", "malicious_count": 0}, "blocklist_de": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Blocklist De", "malicious_count": 0}, "projecthoneypot": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Projecthoneypot", "malicious_count": 0}, "cinsscore_ci_badguys": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Cinsscore Ci Badguys", "malicious_count": 0}, "emergingthreats_compromised_ips": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Emergingthreats Compromised Ips", "malicious_count": 0}, "digitalside_it_hashes": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Digitalside It Hashes", "malicious_count": 0}, "phishstats": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Phishstats", "malicious_count": 0}, "urlhaus": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Urlhaus", "malicious_count": 0}, "sblam_blacklist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Sblam Blacklist", "malicious_count": 0}, "cruz_it_blacklist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Cruz It Blacklist", "malicious_count": 0}, "abuse_ch_sslipbl_aggressive": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Abuse Ch Sslipbl Aggressive", "malicious_count": 0}, "viriback": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Viriback", "malicious_count": 0}, "xroxy": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Xroxy", "malicious_count": 0}, "malc0de": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Malc0de", "malicious_count": 0}, "botscout": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Botscout", "malicious_count": 0}, "rutgers_drop": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Rutgers Drop", "malicious_count": 0}, "spamhaus_edrop": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Spamhaus Edrop", "malicious_count": 0}, "spamhaus_drop": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Spamhaus Drop", "malicious_count": 0}, "digitalside_it_ips": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Digitalside It Ips", "malicious_count": 0}, "urlvir": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Urlvir", "malicious_count": 0}, "the_haleys_ssh_dict_attack": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "The Haleys Ssh Dict Attack", "malicious_count": 0}, "cybercrimetracker_fuckers": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Cybercrimetracker", "malicious_count": 0}, "rulez_blist": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Rulez Blist", "malicious_count": 0}, "azorult-tracker": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Azorult-tracker", "malicious_count": 0}, "phishtank": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Phishtank", "malicious_count": 0}, "name": "Threat Intelligence Feeds", "abuse_ch_sslipbl": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Abuse Ch Sslipbl", "malicious_count": 0}}, "crowdsource": {"response_count": 3, "benign_count": 0, "source_count": 46, "confidence": "low", "name": "Crowdsourced Threat Analysis", "malicious_count": 3}, "tor": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Tor Nodes", "malicious_count": 0}, "name": "Third Party", "misp": {"other": {"response_count": 0, "benign_count": 0, "source_count": 2, "confidence": "Null", "name": "Other", "malicious_count": 0}, "vpn": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Known VPN Hosting Provider", "malicious_count": 0}, "name": "MISP", "dch": {"response_count": 1, "benign_count": 1, "source_count": 6, "confidence": "high", "name": "Dynamic Cloud Hosting (DCH) Provider", "malicious_count": 0}, "sinkhole": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Internet Sinkhole", "malicious_count": 0}, "popular_infra": {"response_count": 0, "benign_count": 0, "source_count": 12, "confidence": "Null", "name": "Popular Internet Infrastructure", "malicious_count": 0}}, "greynoise": {"name": "GreyNoise", "context": {"response_count": 0, "benign_count": 0, "source_count": 1, "confidence": "Null", "name": "Context", "malicious_count": 0}, "riot": {"response_count": 0, "benign_count": 0, "source_count": 2, "confidence": "Null", "name": "RIOT", "malicious_count": 0}}}, "mandiant": {"bp_hosting": {"response_count": 0, "benign_count": 0, "source_count": 2, "confidence": "Null", "name": "Bulletproof Hosting", "malicious_count": 0}, "name": "Mandiant", "malware_analysis": {"response_count": 1, "benign_count": 0, "source_count": 2, "confidence": "med", "name": "Malware Analysis", "malicious_count": 1}, "knowledge_graph": {"response_count": 1, "benign_count": 1, "source_count": 2, "confidence": "high", "name": "Knowledge Graph", "malicious_count": 0}}, "version": "1.0.2"}, "timestamp": "2022-08-04T08:24:35.617+0000"}, "analystVerdict": {"confidenceScore": 50, "verdict": "unknown", "reasoning": {"malicious": {"nucleus": ["sig:detect"]}, "benign": {"nucleus": ["omit:parkip"]}}, "timestamp": "2022-08-04T08:02:23.914+0000"}, "authoritativeVerdict": "analystVerdict"}, "misp": {"smtp-receiving-ips": "False", "covid": "False", "eicar.com": "False", "majestic_million": "False", "sinkholes": "False", "alexa": "False", "cisco_top1000": "False", "microsoft": "False", "microsoft-office365": "False", "crl-hostname": "False", "googlebot": "False", "microsoft-azure-germany": "False", "microsoft-attack-simulator": "False", "microsoft-azure": "False", "rfc5735": "False", "tranco10k": "False", "dax30": "False", "public-dns-v4": "False", "dynamic-dns": "False", "public-dns-v6": "False", "covid-19-cyber-threat-coalition-whitelist": "False", "common-ioc-false-positive": "False", "cisco_1M": "False", "google-gmail-sending-ips": "False", "microsoft-azure-china": "False", "stackpath": "False", "google": "False", "cloudflare": "False", "moz-top500": "False", "tranco": "False", "tlds": "False", "university_domains": "False", "smtp-sending-ips": "False", "cisco_top20k": "False", "empty-hashes": "False", "nioc-filehash": "False", "amazon-aws": "False", "url-shortener": "False", "microsoft-office365-ip": "False", "microsoft-win10-connection-endpoints": "False", "microsoft-azure-us-gov": "False", "majestic_million_1M": "False", "mozilla-CA": "False", "whats-my-ip": "False", "microsoft-office365-cn": "False", "vpn-ipv6": "False", "rfc3849": "False", "rfc6761": "False", "security-provider-blogpost": "False", "cisco_top5k": "False", "apple": "False", "public-dns-hostname": "False", "mozilla-IntermediateCA": "False", "rfc1918": "False", "ti-falsepositives": "False", "akamai": "False", "bank-website": "False", "alexa_1M": "False", "automated-malware-analysis": "False", "rfc6598": "False", "google-gcp": "True", "ovh-cluster": "False", "multicast": "False", "phone_numbers": "False", "fastly": "False", "cisco_top10k": "False", "second-level-tlds": "False", "wikimedia": "False", "disposable-email": "False", "common-contact-emails": "False", "vpn-ipv4": "False", "ipv6-linklocal": "False", "covid-19-krassi-whitelist": "False", "crl-ip": "False"}, "id": "ipv4--a18762d7-7a11-5fbc-8011-d503f8e46c7d", "type": "ipv4", "value": "34.102.136.180", "is_publishable": "True", "last_updated": "2022-08-04T08:26:33.431Z"}}, "dataType": "ip", "external_reference": {"source_name": "Mandiant_Connector", "url": "N/A"}, "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"}

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key":"aaa",
        "pwd":"zzz"
    }
}
Response = namedtuple('Response', ['data', 'code'])

class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string

class MandiantHttpResponse:
    def __init__(self, obj, response_code):
        self.code = response_code
        self.object = obj

    def read(self):
        return self.object

@patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestMandiantConnection(unittest.TestCase, object):
    @patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.ping_mandiant')
    async def test_mandiant_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mock_ping_response.return_value = Response({"success":True}, 200)

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        ping_response = await transmission.ping()
        assert ping_response is not None
        assert ping_response['success']
    
    @patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.ping_mandiant')
    def test_mandiant_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = MandiantHttpResponse(response, 400)
        mock_ping_response.side_effect = Exception('a mock-exception occurred while retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_mandiant_results(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)        

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]
        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list
    
    @patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_mandiant_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        mock_result_connection.side_effect = Exception('a mock-exception occurred while retriving ping information')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'
    
    def test_mandiant_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is True
        assert 'status' in query_response, query_response['status'] == 'COMPLETED'
        assert 'progress' in query_response, query_response['progress'] == 100
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_status_connection', autospec=True)
    def test_mandiant_status_exception(self, mock_status_response, mock_api_client):
        error_msg = 'a mock-exception occurred while checking the status'
        mock_api_client.return_value = None
        mock_status_response.return_value = {'status':'FAILED', 'success':False}
        mock_status_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_query_connection', autospec=True)
    def test_mandiant_query_exception(self, mock_query_response, mock_api_client):
        error_msg = 'a mock-exception occurred, cannot create a query connection'
        mock_api_client.return_value = None
        mock_query_response.return_value = {'search_id':'', 'success':False}
        mock_query_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    
    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
    
    @patch('stix_shifter_modules.mandiant.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'a mock-exception occurred while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_ip_response(self, mock_api_client):
        mock_api_client.return_value = None
        data_dict = dict(data="34.102.136.180", data_type="ip")
        ns_data = SimpleNamespace(**data_dict)
        response = prepare_response(ns_data, DATA['report']['full'])
        assert 'code' in response
        assert 'data' in response
        response_data = response['data']
        assert 'success' in response_data and response_data['success'] is True

    def test_hash_response(self, mock_api_client):
        transmitData = {
                            "pulse_count": 1,
                            "pulses": [
                                {
                                    "id": "5e75339d7a27fae2208e680f",
                                    "name": "Abuse.ch Malware Bazaar SHA256 Hashes 3-20-2020",
                                    "description": "Hashes submitted to the Malware Bazaar",
                                    "modified": "2020-03-20T21:20:29.934000",
                                    "created": "2020-03-20T21:20:29.934000",
                                    "tags": [],
                                    "references": [
                                        "http://www.forensickb.com/2013/03/file-entropy-explained.html",
                                        "http://virii.es/U/Using%20Entropy%20Analysis%20to%20Find%20Encrypted%20and%20Packed%20Malware.pdf"
                                    ],
                                    "author": {
                                        "username": "Coretelligent-OTX",
                                        "id": "48983",
                                        "avatar_url": "https://otx.alienvault.com/assets/images/default-avatar.png",
                                        "is_subscribed": False,
                                        "is_following": False
                                    },
                                    "indicator_type_counts": {
                                        "FileHash-SHA256": 1337
                                    },
                                    "indicator_count": 1337,
                                    "is_author": False,
                                    "is_subscribing": None,
                                    "subscriber_count": 182,
                                    "modified_text": "713 days ago ",
                                    "is_modified": False,
                                    "groups": [],
                                    "in_group": False,
                                    "threat_hunter_scannable": True,
                                    "threat_hunter_has_agents": 1,
                                    "related_indicator_type": "FileHash-SHA256",
                                    "related_indicator_is_active": 1
                                }
                            ],
                            "malware": {},
                            "page_type": "PEXE",
                            "sha1": "4b1fc10818dd534922feef4d521eb3574337e3c0",
                            "sha256": "094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d",
                            "md5": "2f6432c5af8d10b04caed90d410ec7ad",
                            "file_class": "PEXE",
                            "file_type": "PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows",
                            "filesize": 472064,
                            "ssdeep": "12288:GCU4gtAxIflaBAFGWf1yN6OcsiUIpqpcsHs4d8/U:MwIflaBaIH2Us69d88",
                            "combined_score": 6.4,
                            "alerts": [
                                {
                                    "families": [],
                                    "description": "Queries for the computername",
                                    "ttp": {},
                                    "name": "antivm_queries_computername",
                                    "markcount": 2,
                                    "references": [
                                        "http://www.forensickb.com/2013/03/file-entropy-explained.html",
                                        "http://virii.es/U/Using%20Entropy%20Analysis%20to%20Find%20Encrypted%20and%20Packed%20Malware.pdf"
                                    ],
                                    "marks": [
                                        {
                                            "pid": 2372,
                                            "cid": 45373,
                                            "call": {
                                                "category": "misc",
                                                "status": 1,
                                                "stacktrace": [],
                                                "api": "GetComputerNameA",
                                                "return_value": 1,
                                                "arguments": {
                                                    "computer_name": "DRXCEBIU"
                                                },
                                                "time": "2020-02-14T23:21:23.187250",
                                                "tid": 2412,
                                                "flags": {}
                                            },
                                            "type": "call"
                                        },
                                        {
                                            "pid": 2372,
                                            "cid": 45374,
                                            "call": {
                                                "category": "misc",
                                                "status": 1,
                                                "stacktrace": [],
                                                "api": "GetComputerNameW",
                                                "return_value": 1,
                                                "arguments": {
                                                    "computer_name": "DRXCEBIU"
                                                },
                                                "time": "2020-02-14T23:21:23.187250",
                                                "tid": 2412,
                                                "flags": {}
                                            },
                                            "type": "call"
                                        }
                                    ],
                                    "severity": 1
                                }
                            ]
                        }
        mock_api_client.return_value = None
        data_dict = dict(data="2f6432c5af8d10b04caed90d410ec7ad", data_type="hash")
        ns_data = SimpleNamespace(**data_dict)
        response = prepare_response(ns_data, transmitData)
        assert 'code' in response
        assert 'data' in response
        response_data = response['data']
        assert 'success' in response_data and response_data['success'] is True

    def test_url_respose(self, mock_api_client):
        transmitData = {
                            "pulse_count": 0,
                            "pulses": [],
                            "alexa": "http://www.alexa.com/siteinfo/safaricom.co.ke",
                            "whois": "http://whois.domaintools.com/safaricom.co.ke",
                            "other_malware_families": [
                                "bot",
                                "spam"
                            ],
                            "url_list": [
                                {
                                    "url": "https://safaricom.co.ke",
                                    "result": {
                                        "urlworker": {
                                            "url": "https://safaricom.co.ke",
                                            "ip": "45.223.18.17",
                                            "filemagic": "HTML document, UTF-8 Unicode text, with very long lines, with CRLF, CR, LF line terminators",
                                            "filetype": "text/html",
                                            "fileclass": "HTML",
                                            "md5": "07c684b6fa56328ea7d3146485085d2d",
                                            "sha256": "191f1c4e93e19ded7d7a8275ed80bf51fe0bf587acd29d49c4872bbdda67f86c",
                                            "http_code": 200,
                                            "http_response": {
                                                "CONTENT-TYPE": "text/html; charset=utf-8",
                                                "TRANSFER-ENCODING": "chunked",
                                                "X-CONTENT-TYPE-OPTIONS": "nosniff",
                                                "CONTENT-SECURITY-POLICY": "script-src 'self' 'unsafe-inline' 'unsafe-eval' *.blaze.co.ke polyfill.io unpkg.com *.facebook.net *.licdn.com *.mystocks.co.ke *.pusher.com *.googletagmanager.com *.youtube.com maps.gstatic.com *.googleapis.com *.google-analytics.com cdnjs.cloudflare.com  *.google.com googletagmanager.com cdn.jsdelivr.net *.fontawesome.com *.safaricom.co.ke *.safaricom.com; worker-src 'self' blob:",
                                                "REFERRER-POLICY": "same-origin",
                                                "X-CACHE": "Miss from cloudfront",
                                                "VIA": "1.1 e95ec8f1dc02e32f0cb9e113963ceb4e.cloudfront.net (CloudFront)",
                                                "X-AMZ-CF-POP": "SEA73-P1",
                                                "X-AMZ-CF-ID": "_mo5n2bEhoarr10W89APPVc0ozE1DXvaTasgDp7hRfM1uoxWdtdOag==",
                                                "X-CDN": "Imperva",
                                                "X-IINFO": "14-139450094-139450099 SNNN RT(1641633694358 417) q(0 0 0 -1) r(3 3) U12"
                                            },
                                            "cert": {
                                                "issuer": {
                                                    "country_name": "BE",
                                                    "organization_name": "GlobalSign nv-sa",
                                                    "common_name": "GlobalSign Atlas R3 DV TLS CA H2 2021"
                                                },
                                                "issuer_str": "Common Name: GlobalSign Atlas R3 DV TLS CA H2 2021, Organization: GlobalSign nv-sa, Country: BE",
                                                "subject": {
                                                    "common_name": "imperva.com"
                                                },
                                                "subject_str": "Common Name: imperva.com",
                                                "subject_alt_names": [
                                                    "testjazz.safaricom.ke",
                                                    "testnewsroom.safaricom.ke",
                                                    "testtwaweza.safaricom.ke",
                                                    "testchapadimba.safaricom.ke",
                                                    "tracetogetherke.com",
                                                    "imperva.com"
                                                ],
                                                "subject_alt_names_str": "testjazz.safaricom.ke, *.tracetogetherke.com, mpesafoundation.safaricom.ke, testfoundation.safaricom.ke, testeliud159.safaricom.ke, testnewsroom.safaricom.ke, testtwaweza.safaricom.ke, testchapadimba.safaricom.ke, tracetogetherke.com, imperva.com",
                                                "fingerprint_sha1": "3B DD 45 53 FA AD E9 7C 76 51 D8 C2 E9 8D F7 06 DE 82 CC 81",
                                                "fingerprint_sha256": "96 9F B6 BA 73 99 A8 54 E3 B7 57 26 64 43 B8 29 41 44 F8 BC C3 44 29 3A A2 D5 78 93 BF F6 72 A1",
                                                "public_key": "AF5F77EBA08E907C9C02C4768E42BD2E5DA289981C04105CC259427C89C34CFE886632EA966BF0A884A1CD257788AD6582C3CCA4E0B19EAFE3BB66DC79A615F6BCB755848526552BDA78EAFFAB370A0796752702FAD465447AECE56CD9A996EA5008D11E53FCF6867C33643695237258EFEB4D289E6E98045EC4145A3DC5DFA846334F59B5FAB87957DAF7D3C06821F2BCBC8230ACFCC6E5AE103F1CFF3F411C864E5BF3DB165AF2C582FD9854AA1BBD367FCF469329A670DB059A0A66A8428504A08CEA359DCF6DF7533FE639B2B21A13AA59E9DD85C1913AAA37ABD157A87975A1F8F16299C27239CBD57612F996FFA327A9B69BD22735C85453DEB41E37A7",
                                                
                                                "signature": "2BEEE3A60066A8F1821840D4F719F98B7F5D6F38123A807171270F97B6DC343867718DA18FA85915637D7927480468ED10C96C04B64C319DABB3D9A3E92C9AC28493D44FE0C4D842C9A0E06EB8D560F55167A21B0A52B8870BD997FB7DB99BE5B30142EFE09A37AB9228B383953BE0948FBA44A7E85CBA2CA5D0184A864E5C294BA063F649C0CC92900914251F3C3AC6CDD3CD090ABF9842630AA0703909E3510BB2A8A73ED6627C02B5D361989FAD8CC433964156D7C31B6457530C236EE57BDF71AA4ED6869FB914306B482F7B02487C1360C09D5F86DF782AE05E9367531F291961D945ACD7D6DF45A293F0045834EE7D5924F200B90F71691761A42D7AE9",
                                                "signature_str": "2B EE E3 A6 00 66 A8 F1 82 18 40 D4 F7 19 F9 8B 7F 5D 6F 38 12 3A 80\n71 71 27 0F 97 B6 DC 34 38 67 71 8D A1 8F A8 59 15 63 7D 79 27 48 04\n68 ED 10 C9 6C 04 B6 4C 31 9D AB B3 D9 A3 E9 2C 9A C2 84 93 D4 4F E0\nC4 D8 42 C9 A0 E0 6E B8 D5 60 F5 51 67 A2 1B 0A 52 B8 87 0B D9 97 FB\n7D B9 9B E5 B3 01 42 EF E0 9A 37 AB 92 28 B3 83 95 3B E0 94 8F BA 44\nA7 E8 5C BA 2C A5 D0 18 4A 86 4E 5C 29 4B A0 63 F6 49 C0 CC 92 90 09\n14 25 1F 3C 3A C6 CD D3 CD 09 0A BF 98 42 63 0A A0 70 39 09 E3 51 0B\nB2 A8 A7 3E D6 62 7C 02 B5 D3 61 98 9F AD 8C C4 33 96 41 56 D7 C3 1B\n64 57 53 0C 23 6E E5 7B DF 71 AA 4E D6 86 9F B9 14 30 6B 48 2F 7B 02\n48 7C 13 60 C0 9D 5F 86 DF 78 2A E0 5E 93 67 53 1F 29 19 61 D9 45 AC\nD7 D6 DF 45 A2 93 F0 04 58 34 EE 7D 59 24 F2 00 B9 0F 71 69 17 61 A4\n2D 7A E9",
                                                "signature_algorithm": "sha256_rsa",
                                                "x509_version": "v3",
                                                "serial_number": "0128CD9DE4779A71330CCEF5DDDF833C",
                                                "serial_number_str": "01 28 CD 9D E4 77 9A 71 33 0C CE F5 DD DF 83 3C",
                                            
                                                "extensions": {
                                                    "subjectAltName": "DNS:testjazz.safaricom.ke, DNS:*.tracetogetherke.com, DNS:mpesafoundation.safaricom.ke, DNS:testfoundation.safaricom.ke, DNS:testeliud159.safaricom.ke, DNS:testnewsroom.safaricom.ke, DNS:testtwaweza.safaricom.ke, DNS:testchapadimba.safaricom.ke, DNS:tracetogetherke.com, DNS:imperva.com",
                                                    "keyUsage": "Digital Signature, Key Encipherment",
                                                    "extendedKeyUsage": "TLS Web Server Authentication, TLS Web Client Authentication",
                                                    "subjectKeyIdentifier": "90:73:31:C9:C3:AE:D3:FD:EE:40:54:79:63:8F:D3:21:EB:7F:5D:BF",
                                                    "certificatePolicies": "Policy: 2.23.140.1.2.1 Policy: 1.3.6.1.4.1.4146.10.1.3   CPS: https://www.globalsign.com/repository/",
                                                    "basicConstraints": "CA:False",
                                                    "authorityInfoAccess": "OCSP - URI:http://ocsp.globalsign.com/ca/gsatlasr3dvtlscah22021 CA Issuers - URI:http://secure.globalsign.com/cacert/gsatlasr3dvtlscah22021.crt",
                                                    "authorityKeyIdentifier": "keyid:2A:34:B9:AA:FA:BF:3C:88:F1:47:F2:D2:12:78:BE:C5:E5:AA:B0:69",
                                                    "crlDistributionPoints": "Full Name:   URI:http://crl.globalsign.com/ca/gsatlasr3dvtlscah22021.crl",
                                                    "ct_precert_scts": "Signed Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 46:A5:55:EB:75:FA:91:20:30:B5:A2:89:69:F4:F3:7D:\n                11:2C:41:74:BE:FD:49:B8:85:AB:F2:FC:70:FE:6D:47\n    Timestamp : Oct 27 00:40:55.923 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:44:02:20:1A:E3:0F:5B:DC:84:37:25:E8:F6:0B:DA:\n                E3:27:F1:8D:3A:0D:7B:54:31:5E:76:2D:28:1A:F3:AD:\n                BD:4F:01:82:02:20:6E:FE:1B:9D:FA:6A:37:21:29:DA:\n                79:8F:70:BE:53:29:5B:12:63:89:06:7D:A2:17:66:41:\n                5E:97:1D:01:0F:93\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 41:C8:CA:B1:DF:22:46:4A:10:C6:A1:3A:09:42:87:5E:\n                4E:31:8B:1B:03:EB:EB:4B:C7:68:F0:90:62:96:06:F6\n    Timestamp : Oct 27 00:40:56.013 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:45:02:21:00:E9:2E:52:C2:D9:D1:41:ED:38:69:4B:\n                B9:34:9C:7F:B9:DC:55:65:B9:5F:C7:BD:1A:B7:3A:BA:\n                88:A6:DC:58:D3:02:20:4B:D1:A6:81:77:B9:F1:CC:9A:\n                53:92:3B:F4:36:66:88:F5:2E:8F:2D:0E:16:F2:E8:D2:\n                64:B2:82:94:DD:69:0E\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : DF:A5:5E:AB:68:82:4F:1F:6C:AD:EE:B8:5F:4E:3E:5A:\n                EA:CD:A2:12:A4:6A:5E:8E:3B:12:C0:20:44:5C:2A:73\n    Timestamp : Oct 27 00:40:56.039 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:46:02:21:00:FE:AD:D9:FA:66:20:4B:13:B1:5B:64:\n                C1:63:46:7B:13:99:83:D7:C1:49:C8:B4:EF:C8:6F:00:\n                AA:56:70:0A:E0:02:21:00:ED:E6:61:71:D6:E6:87:57:\n                7F:71:1E:31:A0:5F:F5:74:3F:9D:1B:30:26:23:3D:9A:\n                87:A6:26:85:85:62:EF:7B"
                                                },
                                                "extensions_str": "Extension 1, name=subjectAltName, value=DNS:testjazz.safaricom.ke, DNS:*.tracetogetherke.com, DNS:mpesafoundation.safaricom.ke, DNS:testfoundation.safaricom.ke, DNS:testeliud159.safaricom.ke, DNS:testnewsroom.safaricom.ke, DNS:testtwaweza.safaricom.ke, DNS:testchapadimba.safaricom.ke, DNS:tracetogetherke.com, DNS:imperva.com\nExtension 2, name=keyUsage, value=Digital Signature, Key Encipherment\nExtension 3, name=extendedKeyUsage, value=TLS Web Server Authentication, TLS Web Client Authentication\nExtension 4, name=subjectKeyIdentifier, value=90:73:31:C9:C3:AE:D3:FD:EE:40:54:79:63:8F:D3:21:EB:7F:5D:BF\nExtension 5, name=certificatePolicies, value=Policy: 2.23.140.1.2.1 Policy: 1.3.6.1.4.1.4146.10.1.3   CPS: https://www.globalsign.com/repository/\nExtension 6, name=basicConstraints, value=CA:False\nExtension 7, name=authorityInfoAccess, value=OCSP - URI:http://ocsp.globalsign.com/ca/gsatlasr3dvtlscah22021 CA Issuers - URI:http://secure.globalsign.com/cacert/gsatlasr3dvtlscah22021.crt\nExtension 8, name=authorityKeyIdentifier, value=keyid:2A:34:B9:AA:FA:BF:3C:88:F1:47:F2:D2:12:78:BE:C5:E5:AA:B0:69\nExtension 9, name=crlDistributionPoints, value=Full Name:   URI:http://crl.globalsign.com/ca/gsatlasr3dvtlscah22021.crl\nExtension 10, name=ct_precert_scts, value=Signed Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 46:A5:55:EB:75:FA:91:20:30:B5:A2:89:69:F4:F3:7D:\n                11:2C:41:74:BE:FD:49:B8:85:AB:F2:FC:70:FE:6D:47\n    Timestamp : Oct 27 00:40:55.923 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:44:02:20:1A:E3:0F:5B:DC:84:37:25:E8:F6:0B:DA:\n                E3:27:F1:8D:3A:0D:7B:54:31:5E:76:2D:28:1A:F3:AD:\n                BD:4F:01:82:02:20:6E:FE:1B:9D:FA:6A:37:21:29:DA:\n                79:8F:70:BE:53:29:5B:12:63:89:06:7D:A2:17:66:41:\n                5E:97:1D:01:0F:93\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : 41:C8:CA:B1:DF:22:46:4A:10:C6:A1:3A:09:42:87:5E:\n                4E:31:8B:1B:03:EB:EB:4B:C7:68:F0:90:62:96:06:F6\n    Timestamp : Oct 27 00:40:56.013 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:45:02:21:00:E9:2E:52:C2:D9:D1:41:ED:38:69:4B:\n                B9:34:9C:7F:B9:DC:55:65:B9:5F:C7:BD:1A:B7:3A:BA:\n                88:A6:DC:58:D3:02:20:4B:D1:A6:81:77:B9:F1:CC:9A:\n                53:92:3B:F4:36:66:88:F5:2E:8F:2D:0E:16:F2:E8:D2:\n                64:B2:82:94:DD:69:0E\nSigned Certificate Timestamp:\n    Version   : v1 (0x0)\n    Log ID    : DF:A5:5E:AB:68:82:4F:1F:6C:AD:EE:B8:5F:4E:3E:5A:\n                EA:CD:A2:12:A4:6A:5E:8E:3B:12:C0:20:44:5C:2A:73\n    Timestamp : Oct 27 00:40:56.039 2021 GMT\n    Extensions: none\n    Signature : ecdsa-with-SHA256\n                30:46:02:21:00:FE:AD:D9:FA:66:20:4B:13:B1:5B:64:\n                C1:63:46:7B:13:99:83:D7:C1:49:C8:B4:EF:C8:6F:00:\n                AA:56:70:0A:E0:02:21:00:ED:E6:61:71:D6:E6:87:57:\n                7F:71:1E:31:A0:5F:F5:74:3F:9D:1B:30:26:23:3D:9A:\n                87:A6:26:85:85:62:EF:7B"
                                            },
                                            "has_file_analysis": False
                                        },
                                        "extractor": {
                                            "title": "<title>Safaricom| Voice | Data | Mpesa | Home Fibre |Postpaid | Prepaid| 4G </title>",
                                            "cookies": [
                                                {
                                                    "bdef7f9ff899a66c10eb12bc6bdcd537": "70alkmkdnpb31417fpquqaie1v",
                                                    "path": "/",
                                                    "HttpOnly": True
                                                }
                                            ]
                                        },
                                        "safebrowsing": {
                                            "matches": []
                                        },
                                        "tlp": "WHITE"
                                    },
                                    "params": {},
                                    "date": "2022-01-08T08:53:32",
                                    "checked": 1,
                                    "deep_analysis": True,
                                    "secs": 1641632012.0,
                                    "httpcode": 200,
                                    "gsb": []
                                }
                            ]
                    }
                            
        mock_api_client.return_value = None
        data_dict = dict(data="https://safaricom.co.ke", data_type="url")
        ns_data = SimpleNamespace(**data_dict)
        response = prepare_response(ns_data, transmitData)
        assert 'code' in response
        assert 'data' in response
        response_data = response['data']
        assert 'success' in response_data and response_data['success'] is True

    def test_domain_response(self, mock_api_client):
        transmitData = {
                            "pulse_count": 0,
                            "pulses": [],
                            "whois": "http://whois.domaintools.com/telkom.co.id",
                            "malware_samples": "-",
                            "url_list": [
                                {
                                    "url": "https://nde.telkom.co.id/nde/print/1792222?token=669913ac70525841624fc82ec4b98d8b",
                                    "date": "2022-02-04T06:19:25",
                                    "domain": "telkom.co.id",
                                    "hostname": "nde.telkom.co.id",
                                    "result": {
                                        "urlworker": {
                                            "ip": "180.250.116.185",
                                            "http_code": 200
                                        },
                                        "safebrowsing": {
                                            "matches": []
                                        }
                                    },
                                    "httpcode": 200,
                                    "gsb": [],
                                    "encoded": "https%3A//nde.telkom.co.id/nde/print/1792222%3Ftoken%3D669913ac70525841624fc82ec4b98d8b"
                                }
                            ],
                            "passive_dns": [
                                {
                                    "address": "180.250.116.185",
                                    "first": "2022-02-04T06:20:16",
                                    "last": "2022-02-04T06:20:18",
                                    "hostname": "nde.telkom.co.id",
                                    "record_type": "A",
                                    "indicator_link": "/indicator/hostname/nde.telkom.co.id",
                                    "flag_url": "assets/images/flags/id.png",
                                    "flag_title": "Indonesia",
                                    "asset_type": "hostname",
                                    "asn": "AS7713 PT Telekomunikasi Indonesia"
                                },
                                {
                                    "address": "180.250.116.93",
                                    "first": "2020-06-03T16:29:45",
                                    "last": "2020-06-03T16:29:45",
                                    "hostname": "myenterprise.telkom.co.id",
                                    "record_type": "A",
                                    "indicator_link": "/indicator/hostname/myenterprise.telkom.co.id",
                                    "flag_url": "assets/images/flags/id.png",
                                    "flag_title": "Indonesia",
                                    "asset_type": "hostname",
                                    "asn": "AS7713 PT Telekomunikasi Indonesia"
                                }
                            ],
                            "verdict": "None",
                            "continent_code": "AS",
                            "country_code": "ID",
                            "country_name": "Indonesia",
                            "city": "Bogor",
                            "asn": "AS7713 PT Telekomunikasi Indonesia"
                        }
                           
        mock_api_client.return_value = None
        data_dict = dict(data="telkom.co.id", data_type="domain")
        ns_data = SimpleNamespace(**data_dict)
        response = prepare_response(ns_data, transmitData)
        assert 'code' in response
        assert 'data' in response
        response_data = response['data']
        assert 'success' in response_data and response_data['success'] is True
