virus_total_test_ip_value = "76.17.106.185"  #benign
virus_total_test_query_pattern = "[ipv4-addr:value='" + virus_total_test_ip_value + "']"

virus_total_test_domain_value = "moncleroutlets.com" #unknown
virus_total_test_query_pattern_domain = "[domain-name:value='" + virus_total_test_domain_value + "']"

virus_total_test_hash_value = "16cda323189d8eba4248c0a2f5ad0d8f"  #mal
virus_total_test_query_pattern_hash = "[file:hashes.MD5='" + virus_total_test_hash_value + "']"

virus_total_test_url = "linkprotect.cudasvc.com/url" #mal
virus_total_test_query_pattern_url = "[url:value='" + virus_total_test_url + "']"

virus_total_transmitQueryData_ip_benign = { 
    "data": [
        {
            "code": 200,
            "data": virus_total_test_ip_value,
            "report": {
                "success": 'true',
                "full": {
                    "data": {
                        "attributes": {
                            "network": "76.16.0.0/12",
                            "tags": [],
                            "country": "US",
                            "as_owner": "COMCAST-7922",
                            "last_analysis_stats": {
                                "harmless": 93,
                                "malicious": 0,
                                "suspicious": 0,
                                "undetected": 0,
                                "timeout": 0
                            },
                            "asn": 7922,
                            "last_analysis_results": {
                                "CMC Threat Intelligence": {
                                    "category": "harmless",
                                    "result": "clean",
                                    "method": "blacklist",
                                    "engine_name": "CMC Threat Intelligence"
                                },
                            },
                            "reputation": 0,
                            "last_modification_date": 1548448577,
                            "regional_internet_registry": "ARIN",
                            "continent": "NA",
                            "total_votes": {
                                "harmless": 0,
                                "malicious": 0
                            }
                        },
                        "type": "ip_address",
                        "id": "76.17.106.185",
                        "links": {
                            "self": "https://www.virustotal.com/api/v3/ip_addresses/76.17.106.185"
                        },
                        "info": {
                            "detected_urls": {
                                "scan_date": "2019-01-25 15:36:17",
                                "positives": 0,
                                "total": 93
                            },
                            "permalink": "https://www.virustotal.com/gui/ip-address/76.17.106.185"
                        }
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "VirusTotal_Connector",
                "url": "https://www.virustotal.com/gui/ip-address/76.17.106.185"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

virus_total_transmitQueryData_hash_mal = {
    "data": [
        {
            "code": 200,
            "data": virus_total_test_hash_value,
            "report": {
                "success": 'true',
                "full": {
                    "data": {
                        "attributes": {
                            "type_description": "Win32 EXE",
                            "tlsh": "T19814BF0F9F8FEA31C1A156BBA53A7303560BC926B1DBE55C23175080E1E496ACF9C763",
                            "vhash": "0250466d15756az13jza0011fz",
                            "trid": [
                                {
                                    "file_type": "Win16 NE executable (generic)",
                                    "probability": 32.3
                                },
                                {
                                    "file_type": "Win32 Executable (generic)",
                                    "probability": 28.9
                                },
                                {
                                    "file_type": "OS/2 Executable (generic)",
                                    "probability": 13.0
                                },
                                {
                                    "file_type": "Generic Win/DOS Executable",
                                    "probability": 12.8
                                },
                                {
                                    "file_type": "DOS Executable Generic",
                                    "probability": 12.8
                                }
                            ],
                            "creation_date": 1400139405,
                            "names": [],
                            "last_modification_date": 1658788828,
                            "type_tag": "peexe",
                            "times_submitted": 3,
                            "total_votes": {
                                "harmless": 0,
                                "malicious": 0
                            },
                            "size": 201126,
                            "popular_threat_classification": {
                                "suggested_threat_label": "trojan.cabby/kryptik",
                                "popular_threat_category": [
                                    {
                                        "count": 21,
                                        "value": "trojan"
                                    }
                                ],
                                "popular_threat_name": [
                                    {
                                        "count": 7,
                                        "value": "cabby"
                                    },
                                    {
                                        "count": 5,
                                        "value": "kryptik"
                                    },
                                    {
                                        "count": 3,
                                        "value": "anunak"
                                    }
                                ]
                            },
                            "authentihash": "785c11726385d6a3f6a74e35be723700b41a1e857c36ae92d72d397a2e9ef24a",
                            "last_submission_date": 1658781486,
                            "reputation": 0,
                            "sha256": "b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953",
                            "type_extension": "exe",
                            "tags": [
                                "peexe",
                                "overlay",
                                "runtime-modules",
                                "long-sleeps",
                                "direct-cpu-clock-access",
                                "nxdomain",
                                "spreader"
                            ],
                            "last_analysis_date": 1658781486,
                            "unique_sources": 3,
                            "first_submission_date": 1471452789,
                            "sha1": "917e60cdb3cd6fac7f476787428cac5045367ce4",
                            "ssdeep": "3072:su2q9BIau/qCVjvoXCwWg2n/pujQiJweZ7SZ1LOlODa4+J3881TZVn3lpgR:OqbQVT5wWgsGJw2WlOeaA81Lnu",
                            "md5": "16cda323189d8eba4248c0a2f5ad0d8f",
                            "pe_info": {
                                "resource_details": [
                                    {
                                        "lang": "ENGLISH US",
                                        "entropy": 7.988400936126709,
                                        "chi2": 2244.1,
                                        "filetype": "unknown",
                                        "sha256": "8343b7fbf531b99b295339a9a0c4266fe82f26c4052ad8ae662e67c398172068",
                                        "type": "Struct(32)"
                                    },
                                    {
                                        "lang": "ENGLISH US",
                                        "entropy": 7.609860420227051,
                                        "chi2": 1680.1,
                                        "filetype": "unknown",
                                        "sha256": "32b2b4ac44c7aa4354d832716c78d004d3dd80124ffb4547402467c53341e73f",
                                        "type": "Struct(32)"
                                    },
                                    {
                                        "lang": "ENGLISH US",
                                        "entropy": 6.758677005767822,
                                        "chi2": 6528.98,
                                        "filetype": "unknown",
                                        "sha256": "131f7cb723f1ad0e5befdd8968b78870a065b5fc677bb003c103efeb557be318",
                                        "type": "Struct(33)"
                                    }
                                ],
                                "resource_types": {
                                    "Struct(33)": 1,
                                    "Struct(32)": 2
                                },
                                "imphash": "72561468b98e8377206b2bf6322f03ea",
                                "overlay": {
                                    "entropy": 3.550229549407959,
                                    "offset": 189440,
                                    "chi2": 540755.38,
                                    "filetype": "unknown",
                                    "md5": "30ab5f4a0a4095f08b1461d1a3c12c9a",
                                    "size": 11686
                                },
                                "resource_langs": {
                                    "ENGLISH US": 3
                                },
                                "machine_type": 332,
                                "timestamp": 1400139405,
                                "entry_point": 30052,
                                "sections": [
                                    {
                                        "name": ".text",
                                        "chi2": 504273.94,
                                        "virtual_address": 4096,
                                        "entropy": 6.5,
                                        "raw_size": 48128,
                                        "flags": "rx",
                                        "virtual_size": 47872,
                                        "md5": "e0e63d9c66076ed88d143450bca60daa"
                                    },
                                    {
                                        "name": ".data",
                                        "chi2": 277803.5,
                                        "virtual_address": 53248,
                                        "entropy": 3.44,
                                        "raw_size": 3072,
                                        "flags": "rw",
                                        "virtual_size": 6969,
                                        "md5": "a223a120c7a2a1c9fa177fbaf28cb386"
                                    },
                                    {
                                        "name": ".rsrc",
                                        "chi2": 2683.62,
                                        "virtual_address": 61440,
                                        "entropy": 7.99,
                                        "raw_size": 129536,
                                        "flags": "r",
                                        "virtual_size": 129426,
                                        "md5": "c490cbd67de6355105eb32c6cca95061"
                                    },
                                    {
                                        "name": ".reloc",
                                        "chi2": 32382.65,
                                        "virtual_address": 192512,
                                        "entropy": 6.71,
                                        "raw_size": 7680,
                                        "flags": "r",
                                        "virtual_size": 7256,
                                        "md5": "43c3569408955139b92f9bedf3e54b54"
                                    }
                                ],
                                "import_list": [
                                    {
                                        "library_name": "kernel32.DLL",
                                        "imported_functions": [
                                            "CloseHandle",
                                            "CreateEventW",
                                            "FileTimeToSystemTime",
                                            "FindResourceA",
                                            "FormatMessageW",
                                            "GetComputerNameW",
                                            "GetConsoleAliasW",
                                            "GetLocalTime",
                                            "GetLogicalDrives",
                                            "GetModuleHandleA",
                                            "GetProcAddress",
                                            "GetStdHandle",
                                            "GetSystemInfo",
                                            "GetTickCount",
                                            "InterlockedDecrement",
                                            "InterlockedExchange",
                                            "lstrcmpA",
                                            "lstrcmpiA",
                                            "VirtualQuery"
                                        ]
                                    },
                                    {
                                        "library_name": "shlwapi.DLL",
                                        "imported_functions": [
                                            "PathCombineA",
                                            "PathCommonPrefixA",
                                            "PathCompactPathA",
                                            "UrlCanonicalizeA",
                                            "UrlEscapeA",
                                            "UrlGetPartA",
                                            "UrlHashA",
                                            "UrlIsA",
                                            "UrlIsOpaqueW",
                                            "UrlUnescapeA"
                                        ]
                                    },
                                    {
                                        "library_name": "cmdial32.DLL",
                                        "imported_functions": [
                                            "CmCustomDialDlg",
                                            "InetDialHandler"
                                        ]
                                    },
                                    {
                                        "library_name": "cfgmgr32.DLL",
                                        "imported_functions": [
                                            "CM_Add_Empty_Log_Conf",
                                            "CM_Add_Range",
                                            "CMP_Report_LogOn"
                                        ]
                                    },
                                    {
                                        "library_name": "user32.DLL",
                                        "imported_functions": [
                                            "CharToOemA",
                                            "DialogBoxParamA",
                                            "DispatchMessageA",
                                            "DrawIcon",
                                            "GetCaretPos",
                                            "GetWindowLongA",
                                            "GetWindowTextA",
                                            "IsCharLowerW",
                                            "IsDialogMessageA",
                                            "IsWindow",
                                            "IsZoomed",
                                            "LoadCursorA",
                                            "LoadImageA",
                                            "PeekMessageA",
                                            "SetCursorPos",
                                            "SetFocus",
                                            "wsprintfA"
                                        ]
                                    },
                                    {
                                        "library_name": "msimg32.DLL",
                                        "imported_functions": [
                                            "AlphaBlend",
                                            "DllInitialize",
                                            "GradientFill",
                                            "TransparentBlt",
                                            "vSetDdrawflag"
                                        ]
                                    }
                                ]
                            },
                            "magic": "PE32 executable for MS Windows (GUI) Intel 80386 32-bit",
                            "last_analysis_stats": {
                                "harmless": 0,
                                "type-unsupported": 4,
                                "suspicious": 0,
                                "confirmed-timeout": 0,
                                "timeout": 0,
                                "failure": 0,
                                "malicious": 54,
                                "undetected": 17
                            },
                            "last_analysis_results": {
                                "Bkav": {
                                    "category": "malicious",
                                    "engine_name": "Bkav",
                                    "engine_version": "1.3.0.9899",
                                    "result": "W32.AIDetect.malware2",
                                    "method": "blacklist",
                                    "engine_update": "20220725"
                                },
                                "CrowdStrike": {
                                    "category": "malicious",
                                    "engine_name": "CrowdStrike",
                                    "engine_version": "1.0",
                                    "result": "win/malicious_confidence_100% (W)",
                                    "method": "blacklist",
                                    "engine_update": "20220418"
                                }
                            },
                            "first_seen_itw_date": 1471433868
                        },
                        "type": "file",
                        "id": "b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953",
                        "links": {
                            "self": "https://www.virustotal.com/api/v3/files/b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953"
                        },
                        "info": {
                            "positives": 54,
                            "resource": "16cda323189d8eba4248c0a2f5ad0d8f",
                            "scan_id": "b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953-1658781486",
                            "sha256": "b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953",
                            "sha1": "917e60cdb3cd6fac7f476787428cac5045367ce4",
                            "md5": "16cda323189d8eba4248c0a2f5ad0d8f",
                            "scan_date": "2022-07-25 16:38:06",
                            "total": 71,
                            "permalink": "https://www.virustotal.com/gui/file/b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953"
                        }
                    }
                }
            },
            "dataType": "hash",
            "external_reference": {
                "source_name": "VirusTotal_Connector",
                "url": "https://www.virustotal.com/gui/file/b28531feb7299e60eabd01b20c1f1e9f79b9f72cbb58bf3df1ccd14e08dbf953"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}     

virus_total_transmitQueryData_domain_none = {
    "data": [
        {
            "code": 200,
            "data": virus_total_test_domain_value,
            "report": {
                "success": 'true',
                "full": {
                    "data": {
                        "attributes": {
                            "last_dns_records": [
                                {
                                    "rname": "hostmaster.sedo.de",
                                    "retry": 10800,
                                    "value": "ns1.sedoparking.com",
                                    "minimum": 86400,
                                    "refresh": 86400,
                                    "expire": 604800,
                                    "ttl": 21600,
                                    "serial": 2018051601,
                                    "type": "SOA"
                                },
                                {
                                    "type": "A",
                                    "value": "64.190.62.111",
                                    "ttl": 300
                                },
                                {
                                    "type": "NS",
                                    "value": "ns2.sedoparking.com",
                                    "ttl": 21600
                                },
                                {
                                    "type": "NS",
                                    "value": "ns1.sedoparking.com",
                                    "ttl": 21600
                                },
                                {
                                    "priority": 0,
                                    "type": "MX",
                                    "value": "localhost",
                                    "ttl": 3600
                                },
                                {
                                    "type": "TXT",
                                    "value": "v=spf1 -all",
                                    "ttl": 3600
                                }
                            ],
                            "jarm": "20d08b20d21d20d20c42d08b20b41d494e0df9532e75299f15ba73156cee38",
                            "whois": "Admin City: Sejong-Shi\nAdmin Country: KR\nAdmin Email: 861f22c6d2ff5443s@naver.com\nAdmin Postal Code: 30063\nAdmin State/Province: SEJONG\nCreation Date: 2012-01-19T19:32:11.000Z\nCreation Date: 2012-01-19T19:32:11Z\nDNSSEC: unsigned\nDomain Name: MONCLEROUTLETS.COM\nDomain Name: moncleroutlets.com\nDomain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited\nDomain Status: clientTransferProhibited https://www.icann.org/epp#clientTransferProhibited\nName Server: NS1.SEDOPARKING.COM\nName Server: NS2.SEDOPARKING.COM\nName Server: ns1.sedoparking.com\nName Server: ns2.sedoparking.com\nRegistrant City: 7c9d875bd403dba1\nRegistrant Country: KR\nRegistrant Email: 861f22c6d2ff5443s@naver.com\nRegistrant Fax Ext: 3432650ec337c945\nRegistrant Fax: 3432650ec337c945\nRegistrant Name: 8af78d82875c3096\nRegistrant Organization: 3432650ec337c945\nRegistrant Phone Ext: 3432650ec337c945\nRegistrant Phone: 6e385ff11f0564e5\nRegistrant Postal Code: f7d6d68b9b825ebd\nRegistrant State/Province: 4aff2b5cf1e6ac1e\nRegistrant Street: 2232a46d46038e17\nRegistrar Abuse Contact Email: abuse@NameBright.com\nRegistrar Abuse Contact Phone: +1.7204960020\nRegistrar IANA ID: 1441\nRegistrar Registration Expiration Date: 2022-01-19T00:00:00.000Z\nRegistrar URL: http://www.NameBright.com\nRegistrar WHOIS Server: whois.namebright.com\nRegistrar WHOIS server: whois.NameBright.com\nRegistrar: TurnCommerce, Inc. DBA NameBright.com\nRegistry Admin ID: Not Available From Registry\nRegistry Domain ID: 1697792293_DOMAIN_COM-VRSN\nRegistry Expiry Date: 2022-01-19T19:32:11Z\nRegistry Registrant ID: Not Available From Registry\nRegistry Tech ID: Not Available From Registry\nTech City: Sejong-Shi\nTech Country: KR\nTech Email: 861f22c6d2ff5443s@naver.com\nTech Postal Code: 30063\nTech State/Province: SEJONG\nUpdated Date: 2020-08-08T00:00:00.000Z\nUpdated Date: 2020-08-08T14:51:58Z",
                            "last_https_certificate_date": 1630767799,
                            "tags": [],
                            "popularity_ranks": {},
                            "last_dns_records_date": 1630767799,
                            "last_analysis_stats": {
                                "harmless": 85,
                                "malicious": 0,
                                "suspicious": 0,
                                "undetected": 9,
                                "timeout": 0
                            },
                            "creation_date": 1327001531,
                            "whois_date": 1630720089,
                            "reputation": 0,
                            "registrar": "TurnCommerce, Inc. DBA NameBright.com",
                            "last_analysis_results": {
                                "CMC Threat Intelligence": {
                                    "category": "harmless",
                                    "result": "clean",
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
                            "last_update_date": 1596898318,
                            "last_modification_date": 1630767799,
                            "last_https_certificate": {
                                "size": 1555,
                                "public_key": {
                                    "rsa": {
                                        "key_size": 2048,
                                        "modulus": "00d0494d10e0647d554eaeda6bf40e22d2629afe157eae782aa5d6a8566e7c0e1cb622478fa24f6d8b52672a90e22698fe2401e6f0ee6af1b786918056e97b0ba937b5bf85461eca6710f3402d44d1ee8f3db946b6fa48b167d4629fe8b49f71bdf5a2ae8a11f01e8a6c26468d82befc48be7ca105764af04d2e2ac15d376d2686748b215345b8cc35d106ad53a1f5c2d8343d2c47cd4e281d21c297abb9900d7b5e4ab072155ffb82086a029286e2e517f064bb0fb240d34db5b9e8784d009c37daa02a32d502bb636795dfb4b944cee5dad1011d7ad7e12981d161615714b2c749cf98cefbf1ee7d1fad948fc29751f123d65716dfeab64400e2ef56a04fe563",
                                        "exponent": "010001"
                                    },
                                    "algorithm": "RSA"
                                },
                                "thumbprint_sha256": "85efcc298c89bed7376f08bc49816143ffdef15ba85a982e7a7fb8dc485842bc",
                                "tags": [],
                                "cert_signature": {
                                    "signature": "19f1b0e0350b78ba545552935c32995f94a42c0206c2a8b51dd206fac7c4a91cdc1509ddd7ad91810d83648ba1a01308af39ebc64c497a1295a7ae9ec12037ad93f0368141d381be63d95d3db2d8bb6de619a00638a33ca4692d612689b12ed5d7b6648f0c0eba2996a8bf5ccdb7ccf1f61e68e0b238843d9fab2ec8eefd0ac8f9a64d47d84b6a35db0367a0bf5aca255a2b22d3d791c3f7395d608945627fcd3df9b00bd0541b681e1f3a190ed43a0d507ba718686866d4dc0cee0878f959aa75b76f0ad10ced48b82dd99203399f208061f249aab04d932834743b540bff23e7a84aa8d0db92e1145c098c752cd196a3c16c01841fc085b4dda70ced3d5ffe",
                                    "signature_algorithm": "sha256RSA"
                                },
                                "validity": {
                                    "not_after": "2022-09-04 23:59:59",
                                    "not_before": "2021-09-04 00:00:00"
                                },
                                "version": "V3",
                                "extensions": {
                                    "certificate_policies": [
                                        "2.23.140.1.2.1"
                                    ],
                                    "extended_key_usage": [
                                        "serverAuth",
                                        "clientAuth"
                                    ],
                                    "authority_key_identifier": {
                                        "keyid": "55744fb2724ff560ba50d1d7e6515c9a01871ad7"
                                    },
                                    "subject_alternative_name": [
                                        "moncleroutlets.com",
                                        "*.moncleroutlets.com"
                                    ],
                                    "tags": [],
                                    "subject_key_identifier": "c1d0af60d5b77050dab0683b2894bc255a94d774",
                                    "key_usage": [
                                        "ff"
                                    ],
                                    "1.3.6.1.4.1.11129.2.4.2": "0482016a01680075002979bef09e393921f056739f63a577e5be577d9c600af8",
                                    "CA": 'true',
                                    "ca_information_access": {
                                        "CA Issuers": "http://cacerts.digicert.com/EncryptionEverywhereDVTLSCA-G1.crt",
                                        "OCSP": "http://ocsp.digicert.com"
                                    }
                                },
                                "signature_algorithm": "sha256RSA",
                                "serial_number": "d992c2c55b6b3b1148e7e0592b73891",
                                "thumbprint": "a15e2c3904ce9fa882b255fa5598c6b3652c12f5",
                                "issuer": {
                                    "C": "US",
                                    "CN": "Encryption Everywhere DV TLS CA - G1",
                                    "O": "DigiCert Inc",
                                    "OU": "www.digicert.com"
                                },
                                "subject": {
                                    "CN": "moncleroutlets.com"
                                }
                            },
                            "categories": {},
                            "total_votes": {
                                "harmless": 0,
                                "malicious": 0
                            }
                        },
                        "type": "domain",
                        "id": "moncleroutlets.com",
                        "links": {
                            "self": "https://www.virustotal.com/api/v3/domains/moncleroutlets.com"
                        },
                        "info": {
                            "detected_urls": {
                                "scan_date": "2021-09-04 11:03:19",
                                "positives": 0,
                                "total": 94
                            },
                            "permalink": "https://www.virustotal.com/gui/domain/moncleroutlets.com"
                        }
                    }
                }
            },
            "dataType": "domain",
            "external_reference": {
                "source_name": "VirusTotal_Connector",
                "url": "https://www.virustotal.com/gui/domain/moncleroutlets.com"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

virus_total_transmitQueryData_ip_anomalous = {
    "data": [
        {
            "code": 200,
            "data": virus_total_test_ip_value,
            "report": {
                "success": 'true',
                "full": {
                    "data": {
                        "attributes": {
                            "network": "76.16.0.0/12",
                            "tags": [],
                            "country": "US",
                            "as_owner": "COMCAST-7922",
                            "last_analysis_stats": {
                                "harmless": 0,
                                "malicious": 0,
                                "suspicious": 90,
                                "undetected": 0,
                                "timeout": 0
                            },
                            "asn": 7922,
                            "last_analysis_results": {
                                "CMC Threat Intelligence": {
                                    "category": "harmless",
                                    "result": "clean",
                                    "method": "blacklist",
                                    "engine_name": "CMC Threat Intelligence"
                                },
                            },
                            "reputation": 0,
                            "last_modification_date": 1548448577,
                            "regional_internet_registry": "ARIN",
                            "continent": "NA",
                            "total_votes": {
                                "harmless": 0,
                                "malicious": 0
                            }
                        },
                        "type": "ip_address",
                        "id": "76.17.106.185",
                        "links": {
                            "self": "https://www.virustotal.com/api/v3/ip_addresses/76.17.106.185"
                        },
                        "info": {
                            "detected_urls": {
                                "scan_date": "2019-01-25 15:36:17",
                                "positives": 0,
                                "total": 93
                            },
                            "permalink": "https://www.virustotal.com/gui/ip-address/76.17.106.185"
                        }
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "VirusTotal_Connector",
                "url": "https://www.virustotal.com/gui/ip-address/76.17.106.185"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

virus_total_transmitQueryData_url_mal = {
    "data": [
        {
            "code": 200,
            "data": virus_total_test_url,
            "report": {
                "success": 'true',
                "full": {
                    "data": {
                        "attributes": {
                            "last_http_response_content_sha256": "e2fa6b937e801e1d2b00bd533d84ab378e209074a49533d4696a3aef8d20666b",
                            "last_http_response_code": 400,
                            "last_analysis_results": {
                                "CMC Threat Intelligence": {
                                    "category": "harmless",
                                    "result": "clean",
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
                            "last_final_url": "https://linkprotect.cudasvc.com/url",
                            "last_http_response_content_length": 552,
                            "url": "http://linkprotect.cudasvc.com/url",
                            "redirection_chain": [
                                "http://linkprotect.cudasvc.com/url"
                            ],
                            "last_analysis_date": 1651734109,
                            "tags": [],
                            "last_analysis_stats": {
                                "harmless": 81,
                                "malicious": 1,
                                "suspicious": 0,
                                "undetected": 10,
                                "timeout": 0
                            },
                            "last_submission_date": 1651734109,
                            "threat_names": [],
                            "last_http_response_headers": {
                                "content-length": "552",
                                "date": "Thu, 05 May 2022 07:01:51 GMT",
                                "strict-transport-security": "max-age=31536000; includeSubDomains",
                                "content-type": "text/html",
                                "connection": "keep-alive",
                                "server": "nginx"
                            },
                            "reputation": 1,
                            "categories": {
                                "Forcepoint ThreatSeeker": "information technology",
                                "Sophos": "information technology",
                                "Comodo Valkyrie Verdict": "media sharing",
                                "BitDefender": "misc"
                            },
                            "last_modification_date": 1651734117,
                            "title": "400 Bad Request",
                            "times_submitted": 51,
                            "first_submission_date": 1497991311,
                            "total_votes": {
                                "harmless": 1,
                                "malicious": 0
                            }
                        },
                        "type": "url",
                        "id": "3f45fcf9a663e8e7672cd5e7a060ee919900a7aa0fcc1820c3d6ff8e9d6b3598",
                        "links": {
                            "self": "https://www.virustotal.com/api/v3/urls/3f45fcf9a663e8e7672cd5e7a060ee919900a7aa0fcc1820c3d6ff8e9d6b3598"
                        },
                        "info": {
                            "positives": 1,
                            "resource": "http://linkprotect.cudasvc.com/url",
                            "scan_id": "3f45fcf9a663e8e7672cd5e7a060ee919900a7aa0fcc1820c3d6ff8e9d6b3598",
                            "scan_date": "2022-05-05 03:01:49",
                            "total": 92,
                            "permalink": "https://www.virustotal.com/gui/url/3f45fcf9a663e8e7672cd5e7a060ee919900a7aa0fcc1820c3d6ff8e9d6b3598"
                        }
                    }
                }
            },
            "dataType": "url",
            "external_reference": {
                "source_name": "VirusTotal_Connector",
                "url": "https://www.virustotal.com/gui/url/3f45fcf9a663e8e7672cd5e7a060ee919900a7aa0fcc1820c3d6ff8e9d6b3598"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}