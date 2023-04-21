from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper

DATA = {
    "code": 200,
    "data": {
        "success": 'True',
        "full": {
            "data": {
                "attributes": {
                            "regional_internet_registry": "ARIN",
                            "network": "20.64.0.0/10",
                            "tags": [],
                            "country": "US",
                            "as_owner": "MICROSOFT-CORP-MSN-AS-BLOCK",
                            "last_analysis_stats": {
                                "harmless": 80,
                                "malicious": 4,
                                "suspicious": 0,
                                "undetected": 10,
                                "timeout": 0
                            },
                            "asn": 8075,
                            "whois_date": 1651598323,
                            "last_analysis_results": {
                                "CMC Threat Intelligence": {
                                    "category": "malicious",
                                    "result": "malware",
                                    "method": "blacklist",
                                    "engine_name": "CMC Threat Intelligence"
                                },
                                "Baidu-International": {
                                    "category": "harmless",
                                    "result": "clean",
                                    "method": "blacklist",
                                    "engine_name": "Baidu-International"
                                }
                            },
                            "reputation": 0,
                            "last_modification_date": 1653039072,
                            "total_votes": {
                                "harmless": 0,
                                "malicious": 0
                            },
                            "continent": "NA",
                            "whois": "NetRange: 20.33.0.0 - 20.128.255.255\nCIDR: 20.48.0.0/12, 20.34.0.0/15, 20.33.0.0/16, 20.64.0.0/10, 20.40.0.0/13, 20.128.0.0/16, 20.36.0.0/14\nNetName: MSFT\nNetHandle: NET-20-33-0-0-1\nParent: NET20 (NET-20-0-0-0-0)\nNetType: Direct Allocation\nOriginAS: \nOrganization: Microsoft Corporation (MSFT)\nRegDate: 2017-10-18\nUpdated: 2021-12-14\nRef: https://rdap.arin.net/registry/ip/20.33.0.0\nOrgName: Microsoft Corporation\nOrgId: MSFT\nAddress: One Microsoft Way\nCity: Redmond\nStateProv: WA\nPostalCode: 98052\nCountry: US\nRegDate: 1998-07-10\nUpdated: 2022-03-28\nComment: To report suspected security issues specific to traffic emanating from Microsoft online services, including the distribution of malicious content or other illicit or illegal material through a Microsoft online service, please submit reports to:\r\nComment: * https://cert.microsoft.com. \r\nComment: \r\nComment: For SPAM and other abuse issues, such as Microsoft Accounts, please contact:\r\nComment: * abuse@microsoft.com. \r\nComment: \r\nComment: To report security vulnerabilities in Microsoft products and services, please contact:\r\nComment: * secure@microsoft.com. \r\nComment: \r\nComment: For legal and law enforcement-related requests, please contact:\r\nComment: * msndcc@microsoft.com\r\nComment: \r\nComment: For routing, peering or DNS issues, please \r\nComment: contact:\r\nComment: * IOC@microsoft.com\nRef: https://rdap.arin.net/registry/entity/MSFT\nOrgTechHandle: MRPD-ARIN\nOrgTechName: Microsoft Routing, Peering, and DNS\nOrgTechPhone: +1-425-882-8080 \nOrgTechEmail: IOC@microsoft.com\nOrgTechRef: https://rdap.arin.net/registry/entity/MRPD-ARIN\nOrgAbuseHandle: MAC74-ARIN\nOrgAbuseName: Microsoft Abuse Contact\nOrgAbusePhone: +1-425-882-8080 \nOrgAbuseEmail: abuse@microsoft.com\nOrgAbuseRef: https://rdap.arin.net/registry/entity/MAC74-ARIN\nOrgTechHandle: IPHOS5-ARIN\nOrgTechName: IPHostmaster, IPHostmaster \nOrgTechPhone: +1-425-538-6637 \nOrgTechEmail: iphostmaster@microsoft.com\nOrgTechRef: https://rdap.arin.net/registry/entity/IPHOS5-ARIN\n"
                        },
                        "type": "ip_address",
                        "id": "20.110.52.48",
                        "links": {
                            "self": "https://otx.alienvault.com/indicator/ip/20.110.52.48"
                        },
                        "info": {
                            "detected_urls": {
                                "scan_date": "2022-05-20 05:31:12",
                                "positives": 4,
                                "total": 94
                            },
                            "permalink": "https://otx.alienvault.com/indicator/ip/20.110.52.48"
                        }
            }
        }
    },
    "data": "20.110.52.48",
    "dataType": "ip"
}

class http_struct:
    def __init__(self):
        self.content = ""
        self.headers = ""
        self.status_code = 0

HTTP_RESPONSE = http_struct()
HTTP_RESPONSE.content = bytearray(b'{"detections": {"antivirus_detections": [], "malicious_benign_ratio": "0 / 0", "ids_detections": []}, "facts": {"verdict": "Whitelisted", "reverse_dns": null, "otx_telemetry_7_days": false, "otx_telemetry_30_days": false, "otx_telemetry_all": false, "unique_cves_7_days": [], "unique_cves_30_days": [], "unique_cves_all": [], "indicator_popularity": 0, "ssl_certificates": [], "number_of_domains_resolving_7_days": 0, "number_of_domains_resolving_30_days": 0, "number_of_domains_resolving_all": 0, "unique_tlds_from_domains_resolving": 0, "number_of_dynamic_dns_in_pdns": 0, "url_indicators_from_the_ip_in_av_pulses": 0, "has_twitter_discussion": false, "ip_classification": "Cloud provider", "has_webserver": false, "has_ssh": false, "has_rdp": false, "has_vnc": false, "has_telnet": false, "has_x11": false, "has_db": [], "open_ports": [], "is_open_proxy": false, "is_known_scanner": false, "is_tor": false, "is_vpn_node": false, "is_mining_pool": false, "is_external_ip_lookout": false, "is_sinkhole": false, "is_mining_node": false, "is_possible_mirai_infected": false, "intelmq_feeds": []}}')
HTTP_RESPONSE.status_code = 200

DATA_TRANS = ResponseWrapper(HTTP_RESPONSE)