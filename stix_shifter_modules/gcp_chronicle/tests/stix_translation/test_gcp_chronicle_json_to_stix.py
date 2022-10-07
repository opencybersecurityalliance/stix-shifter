import unittest
from stix_shifter_modules.gcp_chronicle.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

ENTRY_POINT = EntryPoint()

MODULE = "gcp_chronicle"
options = {}
map_data = ENTRY_POINT.get_results_translator().map_data

COMMON_DATA = {
    "event": {
        "metadata": {
            "productLogId": "10190",
            "eventTimestamp": "2022-06-13T14:14:54.409074800Z",
            "eventType": "NETWORK_CONNECTION",
            "vendorName": "Microsoft",
            "productName": "AdvancedHunting-DeviceNetworkEvents",
            "productEventType": "DeviceNetworkEvents",
            "ingestedTimestamp": "2022-06-14T05:10:46.984602Z"
        },
        "principal": {
            "hostname": "alert-windows",
            "assetId": "DeviceId:4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb",
            "asset": {
                "attribute": {
                    "cloud": {
                        "environment": "GOOGLE_CLOUD_PLATFORM"
                    }
                }
            },
            "location": {
                "countryOrRegion": "United States"
            },
            "user": {
                "userid": "system",
                "windowsSid": "S-1-5-18",
                "emailAddresses": ["test@user.com"]
            },
            "process": {
                "pid": "2788",
                "file": {
                    "sha256": "2b3efaca2e57e433e6950286f7a6fb46ed48411322a26d657e58f02f7d232224",
                    "md5": "53a2c077e868af30525019e9d070eddd",
                    "sha1": "ed68d965d3572218fa5b17b54e7726df3b18dee3",
                    "size": "56352",
                    "fullPath": "c:\\windows\\system32\\svchost.exe"
                },
                "commandLine": "svchost.exe -k utcsvc -p",
                "parentProcess": {
                    "pid": "756",
                    "file": {
                        "fullPath": "services.exe"
                    }
                }
            },
            "ip": [
                "1.0.1.1"
            ],

            "port": 52221,
            "administrativeDomain": "nt authority"
        },
        "target": {
            "url": "v20.events.data.microsoft.com",
            "ip": [
                "1.0.1.2"
            ],
            "port": 443
        },
        "securityResult": [
            {
                "category": "alert",
                "summary": "ConnectionSuccess",
                "action": [
                    "ALLOW"
                ]}],
        "network": {
            "ipProtocol": "TCP",
            "direction": "OUTBOUND"
        }
    }}

DATA_SOURCE = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "gcp_chronicle",
    "identity_class": "events"
}


class TestGcpChronicleResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for google chronicle security translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestGcpChronicleResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == DATA_SOURCE['type']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        return observed_data['objects']

    def test_network_traffic_object(self):
        data = {
            'event': {
                'principal': {
                    'ip': ['1.0.0.3'],
                    'port': 53,
                    'mac': ['6e:b7:31:d5:33:6c'],
                },
                'target': {
                    'ip': ['1.0.0.4'],
                    'port': 1172
                },
                'network': {
                    'sentBytes': '326',
                    'ipProtocol': 'UDP',
                    'applicationProtocol': 'DNS',
                    'direction': 'OUTBOUND',
                    'sessionDuration': '7s',
                    'sessionId': '22588147'
                }
            }}
        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)
        network_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (network_obj is not None), 'network-traffic object type not found'
        assert (network_obj.keys() == {'type', 'src_ref', 'src_port', 'dst_ref', 'dst_port', 'src_byte_count',
                                       'protocols', 'extensions'})
        assert (network_obj['type'] == 'network-traffic')
        assert (network_obj['src_port'] == 53)
        assert (network_obj['dst_port'] == 1172)
        assert (network_obj['protocols'] == ['udp', 'dns'])
        assert (network_obj['extensions']['x-gcp-chronicle-network']['session_duration'] == '7s')
        assert (network_obj['extensions']['x-gcp-chronicle-network']['session_id'] == '22588147')
        assert (network_obj['extensions']['x-gcp-chronicle-network']['direction'] == 'OUTBOUND')

        ip_ref = network_obj['src_ref']
        assert (ip_ref in objects), f"src_ref with key {network_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '1.0.0.3')

        mac_ref = ip_obj['resolves_to_refs']
        for mac in mac_ref:
            assert (mac in objects), f"resolves_to_refs with key {mac} not found"
            mac_obj = objects[mac]
            assert (mac_obj['type'] == 'mac-addr')

        ip_ref = network_obj['dst_ref']
        assert (ip_ref in objects), f"dst_ref with key {network_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '1.0.0.4')

    def test_process_and_file_object(self):
        data = {
            "event": {
                'metadata': {
                    'eventTimestamp': '2022-06-06T11:50:45.777108800Z',
                    'eventType': 'PROCESS_LAUNCH'
                },
                "principal": {
                    "hostname": "alert-windows",
                    "user": {
                        "userid": "system",
                        "windowsSid": "S-1-5-18"
                    },
                    "process": {
                        "pid": "1132",
                        "file": {
                            "sha256": "bc866cfcdda37e24dc2634dc282c7a0e6f55209da17a8fa105b07414c0e7c527",
                            "md5": "911d039e71583a07320b32bde22f8e22",
                            "sha1": "ded8fd7f36417f66eb6ada10e0c0d7c0022986e9",
                            "size": "278528",
                            "fullPath": "c:\\windows\\system32\\cmd.exe"
                        },
                        "commandLine": "cmd.exe /c \"\"C:\\Packages\\Plugins\\Microsoft.Azure.AzureDefenderFor"
                                       "Servers.MDE.Windows\\1.0.0.4\\MdeExtensionHandler.cmd\" enable\"",
                        "parentProcess": {
                            "pid": "3068",
                            "file": {
                                "fullPath": "WindowsAzureGuestAgent.exe"
                            }
                        }
                    },
                    "administrativeDomain": "nt authority"
                },
                "target": {
                    "process": {
                        "pid": "1428",
                        "file": {
                            "sha256": "de96a6e69944335375dc1ac238336066889d9ffc7d73628ef4fe1b1b160ab32c",
                            "md5": "7353f60b1739074eb17c5f4dddefe239",
                            "sha1": "6cbce4a295c163791b60fc23d285e6d84f28ee4c",
                            "size": "448000",
                            "fullPath": "powershell.exe"
                        },
                        "commandLine": "Powershell.exe  -NoProfile -NonInteractive -ExecutionPolicy Bypass "
                                       "-File C:\\Packages\\Plugins\\Microsoft.Azure.AzureDefenderForServers."
                                       "MDE.Windows\\1.0.0.4\\\\MdeExtensionHandler.ps1 -Action enable"
                    },
                    "file": {
                        "fullPath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
                    }
                }
            }}
        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)
        proc_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'process')

        assert (proc_obj is not None), 'process object type not found'
        assert (proc_obj.keys() == {'type', 'creator_user_ref', 'pid', 'binary_ref', 'name', 'command_line',
                                    'parent_ref'})

        assert (proc_obj['type'] == 'process')
        assert (proc_obj['pid'] == 1132)
        assert (proc_obj['name'] == 'cmd.exe')
        assert (proc_obj['command_line'] == 'cmd.exe /c ""C:\\Packages\\Plugins\\Microsoft.Azure.AzureDefender'
                                            'ForServers.MDE.Windows\\1.0.0.4\\MdeExtensionHandler.cmd" enable"')

        user_ref = proc_obj['creator_user_ref']
        assert (user_ref in objects), f"creator_user_ref with key {proc_obj['creator_user_ref']} not found"

        binary_ref = proc_obj['binary_ref']
        assert (binary_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"

        binary = objects[binary_ref]
        assert (binary.keys() == {'type', 'parent_directory_ref', 'name', 'hashes', 'size'})
        assert (binary['name'] == 'cmd.exe')
        assert (binary['hashes']['SHA-256'] == 'bc866cfcdda37e24dc2634dc282c7a0e6f55209da17a8fa105b07414c0e7c527')
        assert (binary['size'] == 278528)
        assert (binary['parent_directory_ref'] in objects), \
            f"binary.parent_directory_ref with key {binary['parent_directory_ref']} not found"
        assert (objects[binary['parent_directory_ref']]['path'] == 'c:\\windows\\system32')

        parent_ref = proc_obj['parent_ref']

        assert (parent_ref in objects), f"parent_ref with key {proc_obj['parent_ref']} not found"
        parent = objects[parent_ref]
        assert (parent['name'] == 'WindowsAzureGuestAgent.exe')
        assert (objects[parent['binary_ref']]['name'] == 'WindowsAzureGuestAgent.exe')

    def test_x_oca_event(self):

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(COMMON_DATA)
        event = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert (event['type']) == 'x-oca-event'
        assert (event['provider']) == 'Microsoft'
        assert (event['created'] == '2022-06-13T14:14:54.409074800Z')
        assert (event['action'] == 'NETWORK_CONNECTION')
        assert (event['agent'] == 'AdvancedHunting-DeviceNetworkEvents')
        assert (event['outcome'] == 'DeviceNetworkEvents')
        for ref in ['host_ref', 'user_ref', 'file_ref', 'process_ref', 'parent_process_ref', 'ip_refs', 'network_ref']:
            references = event[ref]
            if isinstance(references, str):
                assert (references in objects), f"{event[ref]} reference object not found"
            else:
                assert (all(ref_obj in objects for ref_obj in references)), f"one of reference object {event[ref]}" \
                                                                            f" not found "

    def test_x_ibm_finding(self):
        data = {
            'event': {
                'metadata': {
                    'productLogId': '287203',
                    'eventTimestamp': '2022-07-28T07:57:16.074005Z',
                    'eventType': 'NETWORK_CONNECTION'
                },
                'principal': {
                    'ip': ['10.0.18.224'],
                    'asset': {
                        'ip': ['10.0.18.224'],
                        'platformSoftware': {
                            'platform': 'windows',
                            'platformVersion': 'windows 10'
                        }
                    }
                },
                'target': {
                    'ip': ['172.217.169.36'],
                    'port': 443,
                    'location': {
                        'countryOrRegion': 'United Kingdom',
                        'regionLatitude': 55.37805,
                        'regionLongitude': -3.435973
                    },
                    'asset': {
                        'ip': ['172.217.169.36']
                    }
                },
                'securityResult': [{
                    'about': [
                        {
                            'url': 'https://testurl.com'
                        }
                    ],
                    'category': 'alert',
                    'summary': 'Anomalous Connection/1 GiB Outbound',
                    'action': ['UNKNOWN_ACTION'],
                    'severity': 80
                }],
                'network': {
                    'ipProtocol': 'TCP'
                }
            }
        }

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)
        finding = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert (finding is not None), "x-ibm-finding not found"

        assert (finding.keys() == {'type', 'src_ip_ref', 'src_os_ref', 'dst_ip_ref', 'extensions', 'finding_type',
                                   'name', 'severity'})
        assert (finding['type'] == "x-ibm-finding")
        ip_ref = finding['src_ip_ref']
        assert (ip_ref in objects), f"src_ip_ref with key {finding['src_ip_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '10.0.18.224')

        ip_ref = finding['dst_ip_ref']
        assert (ip_ref in objects), f"dst_ip_ref with key {finding['dst_ip_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '172.217.169.36')

        os_ref = finding['src_os_ref']
        assert (os_ref in objects), f"src_os_ref with key {finding['src_os_ref']} not found"
        os_obj = objects[os_ref]
        assert (os_obj.keys() == {'type', 'name', 'version'})
        assert (os_obj['type'] == 'software')
        assert (os_obj['name'] == 'windows')
        assert (os_obj['version'] == 'windows 10')

        url_ref = finding['extensions']['x-gcp-chronicle-security-result']['url_ref']
        assert (url_ref in objects), f"url_ref with key " \
                                     f"{finding['extensions']['x-gcp-chronicle-security-result']['url_ref']} not found"
        url_obj = objects[url_ref]
        assert (url_obj.keys() == {'type', 'value'})
        assert (url_obj['type'] == 'url')
        assert (url_obj['value'] == 'https://testurl.com')

        assert (finding['finding_type'] == 'alert')
        assert (finding['name'] == 'Anomalous Connection/1 GiB Outbound')
        assert (finding['extensions']['x-gcp-chronicle-security-result']['actions_taken'] == ['UNKNOWN_ACTION'])
        assert (finding['severity'] == 80)

    def test_asset_property(self):

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(COMMON_DATA)
        principal_asset = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')

        assert (principal_asset is not None), "principal x-oca-asset not found"
        assert (principal_asset.keys() == {'type', 'hostname', 'ip_refs', 'extensions'})
        assert (principal_asset['type'] == "x-oca-asset")
        principal_ip_refs = principal_asset['ip_refs']
        assert (all(
            ip in objects for ip in principal_ip_refs)), f"one of the ip refs with key {principal_asset['ip_refs']} " \
                                                         f"not found"
        for ip in principal_ip_refs:
            assert (objects[ip]['type'] == 'ipv4-addr')

        assert principal_asset['extensions']['x-gcp-chronicle-asset']['asset_id'] == \
               'DeviceId:4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb'
        assert principal_asset['extensions']['x-gcp-chronicle-asset']['cloud_environment'] == 'GOOGLE_CLOUD_PLATFORM'
        assert principal_asset['extensions']['x-gcp-chronicle-asset']['country_or_region'] == 'United States'

    def test_http_network_and_resource_property(self):
        data = {
            'event': {
                'metadata': {
                    'productLogId': 'skyvfhe9a7a7',
                    'eventTimestamp': '2022-07-11T06:59:02.567386Z',
                    'collectedTimestamp': '2022-07-11T06:59:02.761440419Z',
                    'eventType': 'NETWORK_HTTP',
                    'vendorName': 'Google Cloud Platform',
                    'productName': 'GCP BigQuery',
                    'productEventType': 'google.cloud.bigquery.v2.JobService.InsertJob',
                    'ingestedTimestamp': '2022-07-11T06:59:03.925957Z'
                },
                'principal': {
                    'user': {
                        'emailAddresses': ['1234@developer.gserviceaccount.com']
                    },
                    'ip': ['1.0.0.5'],
                    'location': {
                        'countryOrRegion': 'United States',
                        'regionLatitude': 37.09024,
                        'regionLongitude': -95.71289
                    },
                    'labels': [{
                        'key': 'requestMetadata.callerNetwork',
                        'value': 'Request originated from a GCE VM or an on-prem VM behind a VPN, and the log was'
                                 ' enhanced with additional information : REPLACED'
                    }]
                },
                'target': {
                    'application': 'bigquery.googleapis.com',
                    'resource': {
                        'name': 'batch_JSON2bq',
                        'parent': 'coe_dataset',
                        'resourceType': 'TABLE',
                        'resourceSubtype': 'bigquery'
                    },
                    'cloud': {
                        'environment': 'GOOGLE_CLOUD_PLATFORM',
                        'project': {
                            'name': 'gdc-day0-data-poc'
                        }
                    }
                },
                'securityResult': [{
                    "category": "alert",
                    'categoryDetails': ['projects/gdc-day0-data-poc/logs/cloudaudit.googleapis.com%2Factivity'],
                    'action': ['ALLOW'],
                    'severity': '16',
                    'detectionFields': [{
                        'key': 'resource',
                        'value': 'projects/gdc-day0-data-poc/datasets/coe_dataset/tables/batch_JSON2bq'
                    }, {
                        'key': 'resource_name',
                        'value': 'projects/gdc-day0-data-poc/datasets/coe_dataset/tables/batch_JSON2bq'
                    }]
                }],
                'network': {
                    'applicationProtocol': 'http',
                    'http': {
                        'method': 'google.cloud.bigquery.v2.JobService.InsertJob',
                        'userAgent': 'apache-beam-2.39.0,gzip(gfe)'
                    }
                }
            }}

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)

        http_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (http_obj is not None), "network object is not found"
        assert (http_obj.keys() == {'type', 'src_ref', 'protocols', 'extensions'})
        assert (http_obj['type'] == 'network-traffic')

        assert (http_obj['extensions']['http-ext']['request_method'] == 'google.cloud.bigquery.v2.'
                                                                        'JobService.InsertJob')
        assert (http_obj['extensions']['http-ext']['user_agent'] == 'apache-beam-2.39.0,gzip(gfe)')

        resource_ref = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert (resource_ref is not None), "event object is not found"
        assert (resource_ref['extensions']['x-gcp-chronicle-event']['target_resource_ref'] in objects), \
            f"resource reference object is not found"
        assert (objects[resource_ref['extensions']['x-gcp-chronicle-event']['target_resource_ref']]['type']
                == 'x-gcp-chronicle-resource')

        resource_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'x-gcp-chronicle-resource')
        assert (resource_obj is not None), f"resource object is not found"
        assert (resource_obj.keys() == {'type', 'name', 'resource_type', 'resource_subtype'})
        assert (resource_obj['type'] == 'x-gcp-chronicle-resource')
        assert (resource_obj['name'] == 'batch_JSON2bq')
        assert (resource_obj['resource_type'] == 'TABLE')
        assert (resource_obj['resource_subtype'] == 'bigquery')

    def test_network_dns_property(self):
        data = {
            "event": {
                "metadata": {
                    "productLogId": "1033u5mdga0v",
                    "eventTimestamp": "2022-07-04T22:24:03.915513Z",
                    "collectedTimestamp": "2022-07-04T22:24:05.197143232Z",
                    "eventType": "NETWORK_DNS",
                    "vendorName": "Google Cloud Platform",
                    "productName": "Google Cloud DNS",
                    "ingestedTimestamp": "2022-07-04T22:24:11.207624Z"
                },
                "additional": {
                    "response_code": "NXDOMAIN"
                },
                "principal": {
                    "ip": [
                        "2405:200:1604:1969:78::5"
                    ],
                    "location": {
                        "name": "global"
                    },
                    "resource": {
                        "resourceType": "VIRTUAL_MACHINE"
                    },
                    "cloud": {
                        "environment": "GOOGLE_CLOUD_PLATFORM",
                        "project": {
                            "name": "hostproject-test"
                        }
                    }
                },
                "target": {
                    "ip": [
                        "2001:4860:4802:32::6e"
                    ],
                    "location": {
                        "countryOrRegion": "United States",
                        "regionLatitude": 37.09024,
                        "regionLongitude": -95.71289
                    }
                },
                "network": {
                    "ipProtocol": "UDP",
                    "applicationProtocol": "DNS",
                    "dns": {
                        "questions": [
                            {
                                "name": "www.a2k2.in",
                                "type": 1
                            }
                        ],
                        "authoritative": True,
                        "responseCode": 3
                    }
                }
            }}
        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)
        dns_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (dns_obj is not None), "network object is not found"
        assert (dns_obj.keys() == {'type', 'src_ref', 'dst_ref', 'protocols', 'extensions'})
        assert (dns_obj['type'] == 'network-traffic')
        assert (dns_obj['extensions']['dns-ext']['questions'][0]['type'] == 1)
        assert (dns_obj['extensions']['dns-ext']['response_code'] == 3)
        assert (dns_obj['extensions']['dns-ext']['questions'][0]['name'] == "www.a2k2.in")

    def test_email_property(self):

        data = {
            'event': {
                'metadata': {
                    'productLogId': 'MYhRuvkA0N4NtUSOmiBIumilYcKRlBcy',
                    'eventTimestamp': '2022-06-22T11:19:20Z',
                    'eventType': 'EMAIL_TRANSACTION',
                    'vendorName': 'PROOFPOINT',
                    'productName': 'TAP',
                    'productEventType': 'messagesDelivered',
                    'ingestedTimestamp': '2022-06-22T11:43:29.036379Z'
                },
                'additional': {
                    'headerFrom': 'test user1 <user1@iscgalaxy.com>',
                    'phishScore': 0,
                    'spamScore': 0
                },
                'principal': {
                    'user': {
                        'emailAddresses': ['user1@iscgalaxy.com']
                    },
                    'ip': ['1.0.1.8']
                },
                'target': {
                    'user': {
                        'emailAddresses': ['user2@iscgalaxy.com']
                    }
                },
                'intermediary': [{
                    'user': {
                        'emailAddresses': ['user123@iscgalaxy.com', 'user2@iscgalaxy.com']
                    }
                }],
                'about': [{
                    'file': {
                        'sha256': 'b025e6114db79f3a891740c45ed264231ec77b07ab9e7ff9156b6d73eb35861e',
                        'md5': 'ff357be90b834ed71da60df190124592',
                        'fullPath': 'text.txt',
                        'mimeType': 'text/plain'
                    }
                }],
                'securityResult': [{
                    'about': {
                        'url': 'https://testurl.com'
                    },
                    'category': 'threat',
                    'categoryDetails': ['malware'],
                    'threatName': 'url',
                    'action': ['ALLOW_WITH_MODIFICATION'],
                    'threatId': 'd00309e12e797021511111456056ff434c2b85c908d72b8c0dc138259182b9a0',
                    'threatStatus': 'ACTIVE',
                    'detectionFields': [{
                        'key': 'completelyRewritten',
                        'value': 'True'
                    }]
                }],
                'network': {
                    'email': {
                        'from': '010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-000000@amazonses.com',
                        'to': ['user2@iscgalaxy.com'],
                        'mailId': '010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-000000@email.amazonses.com',
                        'subject': ['https://testurl.com'],
                        'isMultipart': False
                    }
                }
            }}
        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)
        email_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'email-message')
        assert (email_obj is not None), " email message object is not found"
        assert (email_obj.keys() == {'type', 'extensions', 'from_ref', 'to_refs', 'subject', 'is_multipart'})
        assert (email_obj['type'] == 'email-message')
        assert (email_obj['subject'] == 'https://testurl.com')
        assert (email_obj['is_multipart'] is not True)

        from_ref = email_obj['from_ref']
        assert (from_ref in objects), f"from_ref with key {email_obj['from_ref']} not found"
        assert (objects[from_ref].keys() == {'type', 'value'})
        assert (objects[from_ref]['type'] == 'email-addr')
        assert (objects[from_ref]['value'] == '010001818b22f94b-c1c1b98b-16f5-40d0-a911-a7f562a5d1d1-'
                                              '000000@amazonses.com')

        to_refs = email_obj['to_refs']
        assert (all(to_r in objects for to_r in to_refs)), f"to_refs with key {email_obj['to_refs']} not found"
        for to_obj in to_refs:
            assert (objects[to_obj]['type'] == 'email-addr')
            assert (objects[to_obj]['value'] == 'user2@iscgalaxy.com')

        file_ref = email_obj['extensions']['x-gcp-chronicle-email-message']['file_ref']
        assert (file_ref in objects), f"file_ref with key " \
                                      f"{email_obj['extensions']['x-gcp-chronicle-email-message']['file_ref']} " \
                                      f"not found"
        assert (objects[file_ref].keys() == {'type', 'hashes', 'name', 'extensions'})
        assert (objects[file_ref]['type'] == 'file')

    def test_registry_property(self):
        data = {
            'event': {
                'metadata': {
                    'productLogId': '10303',
                    'eventTimestamp': '2022-06-13T14:31:59.655075Z',
                    'eventType': 'REGISTRY_MODIFICATION',
                    'vendorName': 'Microsoft',
                    'productName': 'AdvancedHunting-DeviceRegistryEvents',
                    'productEventType': 'DeviceRegistryEvents',
                    'ingestedTimestamp': '2022-06-14T04:48:32.535773Z'
                },
                'principal': {
                    'hostname': 'alert-windows',
                    'assetId': 'DeviceId:4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb',
                    'user': {
                        'userid': 'system',
                        'windowsSid': 'S-1-5-18'
                    },
                    'process': {
                        'pid': '2272',
                        'file': {
                            'sha256': 'dc6995f97212edf6d7b73bdaa7f6cfc50430d0b081fa1bd48b995f4347f32aa7',
                            'md5': '9079dd01c8d9e2ca2b0d10108f2feda9',
                            'sha1': 'e60fe04143860f887b42fa368a4426856e892f41',
                            'size': '7755352',
                            'fullPath': 'c:\\program files\\windows defender advanced threat protection\\mssense.exe'
                        },
                        'commandLine': '"MsSense.exe"',
                        'parentProcess': {
                            'pid': '756',
                            'file': {
                                'fullPath': 'services.exe'
                            }
                        }
                    },
                    'administrativeDomain': 'nt authority'
                },
                'src': {},
                'target': {
                    'registry': {
                        'registryKey': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection',
                        'registryValues': [{'registryValueName': 'CrashHeartbeat',
                                            'registryValueData': '132996043194369129'
                                            }]

                    }
                },
                'observer': {
                    'cloud': {
                        'project': {
                            'id': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e'
                        }
                    }
                },
                'about': [{
                    'labels': [{
                        'key': 'InitiatingProcessTokenElevation',
                        'value': 'TokenElevationTypeDefault'
                    }, {
                        'key': 'InitiatingProcessIntegrityLevel',
                        'value': 'System'
                    }]
                }],
                'securityResult': [{
                    "category": "alert",
                    'summary': 'RegistryValueSet'
                }]
            }
        }

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)

        registry_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')

        assert (registry_obj is not None), " windows registry key object is not found"
        assert (registry_obj.keys() == {'type', 'key', 'values'})
        assert (registry_obj['type'] == 'windows-registry-key')

        assert (registry_obj['key'] == 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection')
        assert (registry_obj['values'][0]['data'] == '132996043194369129')
        assert (registry_obj['values'][0]['name'] == 'CrashHeartbeat')

    def test_certificate_property(self):
        data = {'event': {
            'metadata': {
                'productLogId': 'CH3QeG4kCxFL8eZrs1',
                'eventTimestamp': '2022-07-17T14:01:26.194646Z',
                'eventType': 'NETWORK_CONNECTION',
                'productEventType': 'bro_ssl',
                'description': 'SSL/TLS handshake info',
                'ingestedTimestamp': '2022-08-03T08:47:52.108774Z',
                'id': 'AAAAAAPkQFNb8/5zI4T/1aiVxAEAAAAABQAAAAIAAAA='
            },
            'principal': {
                'ip': ['192.168.4.37'],
                'port': 58842
            },
            'target': {
                'hostname': 'www.google.com',
                'ip': ['172.217.15.100'],
                'port': 443,
                'location': {
                    'countryOrRegion': 'United States',
                    'regionLatitude': 37.09024,
                    'regionLongitude': -95.71289
                }
            },
            'network': {
                'tls': {
                    'client': {
                        'ja3': '3830b2a4fbcea64e74db382e467f5b3b'
                    },
                    'server': {
                        'ja3s': '907bf3ecef1c987c889946b737b43de8',
                        'certificate': {
                            'subject': 'CN=www.taosecurity.com',
                            'issuer': 'CN=Amazon,OU=Server CA 1B,O=Amazon,C=US'
                        }
                    },
                    'cipher': 'TLS_AES_256_GCM_SHA384',
                    'curve': 'x25519',
                    'version': 'TLSv13',
                    'established': True,
                    'resumed': True
                },
                'applicationProtocol': 'tls'
            }
        }
        }

        objects = TestGcpChronicleResultsToStix.get_observed_data_objects(data)

        tls_obj = TestGcpChronicleResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (tls_obj is not None), "network-traffic object is not found"
        assert (tls_obj.keys() == {'type', 'src_ref', 'src_port', 'dst_ref', 'dst_port', 'extensions', 'protocols'})
        assert (tls_obj['type'] == 'network-traffic')
        assert (tls_obj['extensions']['tls-ext']['client_ja3_hash'] == '3830b2a4fbcea64e74db382e467f5b3b')
        assert (tls_obj['extensions']['tls-ext']['server_ja3_hash'] == '907bf3ecef1c987c889946b737b43de8')
        assert (tls_obj['extensions']['tls-ext']['cipher'] == 'TLS_AES_256_GCM_SHA384')
        assert (tls_obj['extensions']['tls-ext']['elliptical_curve'] == 'x25519')
        assert (tls_obj['extensions']['tls-ext']['version'] == 'TLSv13')
        certificate_ref = tls_obj['extensions']['tls-ext']['server_certificate_ref']

        assert (certificate_ref in objects), f"certificate reference object is not found"
        certificate_obj = objects[certificate_ref]
        assert (certificate_obj.keys() == {'type', 'subject', 'issuer'})
        assert (certificate_obj['type'] == 'x509-certificate')

        assert (certificate_obj['subject'] == 'CN=www.taosecurity.com')
        assert (certificate_obj['issuer'] == 'CN=Amazon,OU=Server CA 1B,O=Amazon,C=US')
