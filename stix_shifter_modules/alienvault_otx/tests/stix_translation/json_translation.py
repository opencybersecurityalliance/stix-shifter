ip_value = "203.190.254.239"  #benign
query_pattern = "[ipv4-addr:value='"+ip_value+"']"

domain_value = "moncleroutlets.com" #unknown
query_pattern_domain = "[domain-name:value='"+domain_value+"']"

hash_value = "16cda323189d8eba4248c0a2f5ad0d8f"  #mal
query_pattern_hash = "[file:hashes.MD5='"+hash_value+"']"

url = "linkprotect.cudasvc.com/url" #anomalous
query_pattern_url = "[url:value='"+url+"']"

transmitQueryData_ip_benign = {
"data": [
    {
        "code": 200,
            "data": ip_value,
            "report": {
                "success": 'true',
                "full": {
                    "whois": "http://whois.domaintools.com/203.190.254.239",
                    "reputation": 0,
                    "indicator": ip_value,
                    "type": "IPv4",
                    "type_title": "IPv4",
                    "base_indicator": {},
                    "pulse_info": {
                        "count": 0,
                        "pulses": [],
                        "references": [],
                        "related": {
                            "alienvault": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            },
                            "other": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            }
                        }
                    },
                    "false_positive": [],
                    "validation": [],
                    "asn": "AS24323 aamra networks limited",
                    "city_data": 'true',
                    "city": 'null',
                    "region": 'null',
                    "continent_code": "AS",
                    "country_code3": "BGD",
                    "country_code2": "BD",
                    "subdivision": 'null',
                    "latitude": 23.7018,
                    "postal_code": 'null',
                    "longitude": 90.3742,
                    "accuracy_radius": 200,
                    "country_code": "BD",
                    "country_name": "Bangladesh",
                    "dma_code": 0,
                    "charset": 0,
                    "area_code": 0,
                    "flag_url": "/assets/images/flags/bd.png",
                    "flag_title": "Bangladesh",
                    "sections": [
                        "general",
                        "geo",
                        "reputation",
                        "url_list",
                        "passive_dns",
                        "malware",
                        "nids_list",
                        "http_scans"
                    ],
                    "detections": {
                        "antivirus_detections": [],
                        "malicious_benign_ratio": "0 / 0",
                        "ids_detections": []
                    },
                    "facts": {
                        "verdict": 'Whitelisted',
                        "reverse_dns": "www.icddrb.org",
                        "otx_telemetry_7_days": 'false',
                        "otx_telemetry_30_days": 'false',
                        "otx_telemetry_all": 'false',
                        "unique_cves_7_days": [],
                        "unique_cves_30_days": [],
                        "unique_cves_all": [],
                        "indicator_popularity": 0,
                        "ssl_certificates": [
                            {
                                "port": 443,
                                "subject": "CN=*.icddrb.org",
                                "issuer": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
                                "ja3": "771,49172,65281-11",
                                "fingerprint": "20:89:ce:2e:e1:11:8c:d8:ec:0b:4c:83:40:ef:10:35:e8:f8:15:6e:18:89:59:7b:c6:a0:af:9b:96:50:80:af"
                            }
                        ],
                        "number_of_domains_resolving_7_days": 0,
                        "number_of_domains_resolving_30_days": 0,
                        "number_of_domains_resolving_all": 3,
                        "unique_tlds_from_domains_resolving": 1,
                        "number_of_dynamic_dns_in_pdns": 0,
                        "url_indicators_from_the_ip_in_av_pulses": 0,
                        "has_twitter_discussion": 'false',
                        "ip_classification": 'null',
                        "has_webserver": 'true',
                        "has_ssh": 'false',
                        "has_rdp": 'false',
                        "has_vnc": 'false',
                        "has_telnet": 'false',
                        "has_x11": 'false',
                        "has_db": [],
                        "open_ports": [
                            80,
                            443
                        ],
                        "is_open_proxy": 'false',
                        "is_known_scanner": 'false',
                        "is_tor": 'false',
                        "is_vpn_node": 'false',
                        "is_mining_pool": 'false',
                        "is_external_ip_lookout": 'false',
                        "is_sinkhole": 'false',
                        "is_mining_node": 'false',
                        "is_possible_mirai_infected": 'false',
                        "intelmq_feeds": []
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "OTXQuery_Connector",
                "url": "https://otx.alienvault.com/indicator/ip/203.190.254.239"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

transmitQueryData_ip_benign_num = {
"data": [
    {
        "code": 200,
            "data": ip_value,
            "report": {
                "success": 'true',
                "full": {
                    "whois": "http://whois.domaintools.com/203.190.254.239",
                    "reputation": 0,
                    "indicator": ip_value,
                    "type": "IPv4",
                    "type_title": "IPv4",
                    "base_indicator": {},
                    "pulse_info": {
                        "count": 0,
                        "pulses": [],
                        "references": [],
                        "related": {
                            "alienvault": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            },
                            "other": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            }
                        }
                    },
                    "false_positive": [],
                    "validation": [],
                    "asn": "AS24323 aamra networks limited",
                    "city_data": 'true',
                    "city": 'null',
                    "region": 'null',
                    "continent_code": "AS",
                    "country_code3": "BGD",
                    "country_code2": "BD",
                    "subdivision": 'null',
                    "latitude": 23.7018,
                    "postal_code": 'null',
                    "longitude": 90.3742,
                    "accuracy_radius": 200,
                    "country_code": "BD",
                    "country_name": "Bangladesh",
                    "dma_code": 0,
                    "charset": 0,
                    "area_code": 0,
                    "flag_url": "/assets/images/flags/bd.png",
                    "flag_title": "Bangladesh",
                    "sections": [
                        "general",
                        "geo",
                        "reputation",
                        "url_list",
                        "passive_dns",
                        "malware",
                        "nids_list",
                        "http_scans"
                    ],
                    "detections": {
                        "antivirus_detections": [],
                        "malicious_benign_ratio": "0 / 0",
                        "ids_detections": []
                    },
                    "facts": {
                        "verdict": 'null',
                        "combined_score": 1,
                        "reverse_dns": "www.icddrb.org",
                        "otx_telemetry_7_days": 'false',
                        "otx_telemetry_30_days": 'false',
                        "otx_telemetry_all": 'false',
                        "unique_cves_7_days": [],
                        "unique_cves_30_days": [],
                        "unique_cves_all": [],
                        "indicator_popularity": 0,
                        "ssl_certificates": [
                            {
                                "port": 443,
                                "subject": "CN=*.icddrb.org",
                                "issuer": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
                                "ja3": "771,49172,65281-11",
                                "fingerprint": "20:89:ce:2e:e1:11:8c:d8:ec:0b:4c:83:40:ef:10:35:e8:f8:15:6e:18:89:59:7b:c6:a0:af:9b:96:50:80:af"
                            }
                        ],
                        "number_of_domains_resolving_7_days": 0,
                        "number_of_domains_resolving_30_days": 0,
                        "number_of_domains_resolving_all": 3,
                        "unique_tlds_from_domains_resolving": 1,
                        "number_of_dynamic_dns_in_pdns": 0,
                        "url_indicators_from_the_ip_in_av_pulses": 0,
                        "has_twitter_discussion": 'false',
                        "ip_classification": 'null',
                        "has_webserver": 'true',
                        "has_ssh": 'false',
                        "has_rdp": 'false',
                        "has_vnc": 'false',
                        "has_telnet": 'false',
                        "has_x11": 'false',
                        "has_db": [],
                        "open_ports": [
                            80,
                            443
                        ],
                        "is_open_proxy": 'false',
                        "is_known_scanner": 'false',
                        "is_tor": 'false',
                        "is_vpn_node": 'false',
                        "is_mining_pool": 'false',
                        "is_external_ip_lookout": 'false',
                        "is_sinkhole": 'false',
                        "is_mining_node": 'false',
                        "is_possible_mirai_infected": 'false',
                        "intelmq_feeds": []
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "OTXQuery_Connector",
                "url": "https://otx.alienvault.com/indicator/ip/203.190.254.239"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

transmitQueryData_hash_mal = {
"data": [
        {
            "code": 200,
            "data": hash_value,
            "report": {
                "success": 'true',
                "full": {
                    "whois": "http://whois.domaintools.com/203.190.254.239",
                    "reputation": 0,
                    "type": "md5",
                    "type_title": "FileHash-MD5",
                    "indicator": hash_value,
                    "base_indicator": {},
                    "pulse_info": {
                        "count": 0,
                        "pulses": [],
                        "references": [],
                        "related": {
                            "alienvault": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            },
                            "other": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            }
                        }
                    },
                    "false_positive": [],
                    "validation": [],
                    "asn": "AS24323 aamra networks limited",
                    "city_data": 'true',
                    "city": 'null',
                    "region": 'null',
                    "continent_code": "AS",
                    "country_code3": "BGD",
                    "country_code2": "BD",
                    "subdivision": 'null',
                    "latitude": 23.7018,
                    "postal_code": 'null',
                    "longitude": 90.3742,
                    "accuracy_radius": 200,
                    "country_code": "BD",
                    "country_name": "Bangladesh",
                    "dma_code": 0,
                    "charset": 0,
                    "area_code": 0,
                    "flag_url": "/assets/images/flags/bd.png",
                    "flag_title": "Bangladesh",
                    "sections": [
                        "general",
                        "geo",
                        "reputation",
                        "url_list",
                        "passive_dns",
                        "malware",
                        "nids_list",
                        "http_scans"
                    ],
                    "detections": {
                        "antivirus_detections": [],
                        "malicious_benign_ratio": "0 / 0",
                        "ids_detections": []
                    },
                    "facts": {
                        "verdict": 'null',
                        "combined_score": 12,
                        "reverse_dns": "www.icddrb.org",
                        "otx_telemetry_7_days": 'false',
                        "otx_telemetry_30_days": 'false',
                        "otx_telemetry_all": 'false',
                        "unique_cves_7_days": [],
                        "unique_cves_30_days": [],
                        "unique_cves_all": [],
                        "indicator_popularity": 0,
                        "ssl_certificates": [
                            {
                                "port": 443,
                                "subject": "CN=*.icddrb.org",
                                "issuer": "C=US, O=DigiCert Inc, CN=DigiCert TLS RSA SHA256 2020 CA1",
                                "ja3": "771,49172,65281-11",
                                "fingerprint": "20:89:ce:2e:e1:11:8c:d8:ec:0b:4c:83:40:ef:10:35:e8:f8:15:6e:18:89:59:7b:c6:a0:af:9b:96:50:80:af"
                            }
                        ],
                        "number_of_domains_resolving_7_days": 0,
                        "number_of_domains_resolving_30_days": 0,
                        "number_of_domains_resolving_all": 3,
                        "unique_tlds_from_domains_resolving": 1,
                        "number_of_dynamic_dns_in_pdns": 0,
                        "url_indicators_from_the_ip_in_av_pulses": 0,
                        "has_twitter_discussion": 'false',
                        "ip_classification": 'null',
                        "has_webserver": 'true',
                        "has_ssh": 'false',
                        "has_rdp": 'false',
                        "has_vnc": 'false',
                        "has_telnet": 'false',
                        "has_x11": 'false',
                        "has_db": [],
                        "open_ports": [
                            80,
                            443
                        ],
                        "is_open_proxy": 'false',
                        "is_known_scanner": 'false',
                        "is_tor": 'false',
                        "is_vpn_node": 'false',
                        "is_mining_pool": 'false',
                        "is_external_ip_lookout": 'false',
                        "is_sinkhole": 'false',
                        "is_mining_node": 'false',
                        "is_possible_mirai_infected": 'false',
                        "intelmq_feeds": []
                    }
                }
            },
            "dataType": "hash",
            "external_reference": {
                "source_name": "OTXQuery_Connector",
                "url": "https://otx.alienvault.com/indicator/file/16cda323189d8eba4248c0a2f5ad0d8f"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}     

transmitQueryData_domain_none = {
"data": [
        {
            "code": 200,
            "data": domain_value,
            "report": {
                "success": 'true',
                "full": {
                    "sections": [
                        "general",
                        "geo",
                        "url_list",
                        "passive_dns",
                        "malware",
                        "whois",
                        "http_scans"
                    ],
                    "whois": "http://whois.domaintools.com/moncleroutlets.com",
                    "alexa": "http://www.alexa.com/siteinfo/moncleroutlets.com",
                    "indicator": domain_value,
                    "type": "domain",
                    "type_title": "Domain",
                    "validation": [],
                    "base_indicator": {},
                    "pulse_info": {
                        "count": 0,
                        "pulses": [],
                        "references": [],
                        "related": {
                            "alienvault": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            },
                            "other": {
                                "adversary": [],
                                "malware_families": [],
                                "industries": []
                            }
                        }
                    },
                    "false_positive": [],
                    "detections": {
                        "antivirus_detections": [],
                        "malicious_benign_ratio": "0 / 0"
                    },
                    "facts": {
                        "verdict": 'null',
                        "ip_verdict": 'null',
                        "ssl_certificates": [],
                        "current_ip_addresses": [
                            "64.190.63.111"
                        ],
                        "current_nameservers": [
                            "ns1.sedoparking.com.",
                            "ns2.sedoparking.com."
                        ],
                        "current_asns": [
                            "AS47846 sedo"
                        ],
                        "current_country_codes": [
                            "DE"
                        ],
                        "domain_resolve_number_of_ips": 1,
                        "domain_resolve_number_of_asns": 1,
                        "dns_resolve_malicious_ip": 'false',
                        "domain_registrar": "TurnCommerce, Inc. DBA NameBright.com",
                        "domain_creation_date": "2012-01-19T19:32:11",
                        "domain_registered_last_100_days": 'false',
                        "otx_telemetry_7_days": 'true',
                        "otx_telemetry_30_days": 'true',
                        "otx_telemetry_all": 'false',
                        "has_webserver": 'false',
                        "has_twitter_discussion": 'false',
                        "number_of_open_source_feeds_referencing_this_domain": 0,
                        "number_of_subdomains": 1,
                        "domain_has_spf": 'true',
                        "domain_not_resolving": 'false',
                        "domain_resolving_to_a_private_range": 'false',
                        "domain_in_alexa_100k": 'false',
                        "domain_in_umbrella_100k": 'false',
                        "urldomain_in_majestic_100k": 'false',
                        "domain_in_akamai_list": 'false',
                        "hostname_is_dynamic_dns": 'false',
                        "domain_number_of_malicious_files_hosted": 0,
                        "domain_number_of_malicious_files_communicating": 0,
                        "domain_safebrowsing_detected": 'false',
                        "domain_blocked_by_umbrella": 'false',
                        "domain_blocked_by_quad9": 'false',
                        "domain_blocked_by_akamai": 'false',
                        "is_ddns_domain": 'false',
                        "domain_has_its_own_nameserver": 'false',
                        "is_open_proxy": 'false',
                        "is_known_scanner": 'false',
                        "is_tor": 'false',
                        "is_vpn_node": 'false',
                        "is_mining_pool": 'false',
                        "is_external_ip_lookout": 'false',
                        "is_sinkhole": 'false',
                        "is_mining_node": 'false',
                        "ip_is_open_proxy": 'false',
                        "ip_is_known_scanner": 'false',
                        "ip_is_tor": 'false',
                        "ip_is_vpn_node": 'false',
                        "ip_is_mining_pool": 'false',
                        "ip_is_external_ip_lookout": 'false',
                        "ip_is_sinkhole": 'false',
                        "ip_is_mining_node": 'false',
                        "urls_from_domain_or_hostname_in_av_pulses": 'false',
                        "domain_suspicious_tld": 'false',
                        "is_filesharing": 'false',
                        "is_common_ocsp": 'false',
                        "has_wordpress": 'false',
                        "has_drupal": 'false',
                        "is_opendir": 'false',
                        "is_punycode": 'false',
                        "is_domain_shortener": 'false',
                        "domain_hosting_phishing": 'false',
                        "suspended_or_parked_domain": 'true',
                        "sauron_suspicious_tag": 'false',
                        "domain_is_dga": 'true',
                        "domain_is_free_hosting": 'null',
                        "has_unicode_homoglyph": 'null'
                    }
                }
            },
            "dataType": "domain",
            "external_reference": {
                "source_name": "OTXQuery_Connector",
                "url": "https://otx.alienvault.com/indicator/url/moncleroutlets.com"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

transmitQueryData_url_anom = {
    "data": [
        {
            "code": 200,
            "data": url,
            "report": {
                "success": 'true',
                "full": {
                    "indicators": {
                        "ip": {},
                        "domain": {
                            "indicator": "cudasvc.com",
                            "whitelisted_message": [
                                {
                                    "source": "akamai",
                                    "message": "Akamai rank: #1106",
                                    "name": "Akamai Popular Domain"
                                },
                                {
                                    "source": "majestic",
                                    "message": "Whitelisted domain cudasvc.com",
                                    "name": "Whitelisted domain"
                                },
                                {
                                    "source": "whitelist",
                                    "message": "Whitelisted domain cudasvc.com",
                                    "name": "Whitelisted domain"
                                }
                            ],
                            "suspicious": 'false',
                            "pulse_count": 2,
                            "passivedns_count": 500,
                            "nids_count": 0,
                            "url_count": 21317,
                            "file_count": 0,
                            "whitelisted": 'true'
                        },
                        "facts": {
                            "verdict": 'null',
                            "combined_score": 5
                        },
                        "hostname": {
                            "indicator": "linkprotect.cudasvc.com",
                            "whitelisted_message": [
                                {
                                    "source": "akamai",
                                    "message": "Akamai rank: #1106",
                                    "name": "Akamai Popular Domain"
                                },
                                {
                                    "source": "whitelist",
                                    "message": "Whitelisted domain cudasvc.com",
                                    "name": "Whitelisted domain"
                                },
                                {
                                    "source": "majestic",
                                    "message": "Whitelisted domain cudasvc.com",
                                    "name": "Whitelisted domain"
                                },
                                {
                                    "source": "false_positive",
                                    "message": "Known False Positive",
                                    "name": "Known False Positive"
                                }
                            ],
                            "suspicious": 'false',
                            "pulse_count": 0,
                            "passivedns_count": 496,
                            "nids_count": 0,
                            "url_count": 20369,
                            "file_count": 0,
                            "whitelisted": 'true'
                        }
                    },
                    "stats": {
                        "indicators_with_pulses": {
                            "alienvault": 0,
                            "other": 0
                        }
                    }
                }
            },
            "dataType": "url",
            "external_reference": {
                "source_name": "OTXQuery_Connector",
                "url": "https://otx.alienvault.com/indicator/url/linkprotect.cudasvc.com/url"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}