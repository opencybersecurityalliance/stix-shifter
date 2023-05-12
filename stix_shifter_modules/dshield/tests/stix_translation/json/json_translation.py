dshield_test_ip_value = "101.81.5.6"
dshield_test_query_pattern = "[ipv4-addr:value='" + dshield_test_ip_value + "']"

dshield_test_transmitQueryData_ip_benign = {
    "data": [
        {
            "code": 200,
            "data": "101.81.5.6",
            "report": {
                "success": 'true',
                "full": {
                    "threatfeedscount": 0,
                    "ioc_report": {
                        "number": "101.81.5.6",
                        "maxdate": 'null',
                        "mindate": 'null',
                        "updated": 'null',
                        "comment": 'null',
                        "count": 0,
                        "attacks": 0,
                        "maxrisk": 0,
                        "asabusecontact": "anti-spam@ns.chinanet.cn.net",
                        "as": 4812,
                        "asname": "CHINANET-SH-AP China Telecom Group",
                        "ascountry": "CN",
                        "assize": 11671552,
                        "network": "101.80.0.0/13"
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "DShield_Connector",
                "url": "https://isc.sans.edu/ipinfo.html?ip=101.81.5.6"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

dshield_test_transmitQueryData_ip_unkown = {
     "data": [
        {
            "code": 200,
            "data": "101.81.5.6",
            "report": {
                "success": 'true',
                "full": {
                    "ioc_report": {
                        "number": "101.81.5.6",
                        "maxdate": 'null',
                        "mindate": 'null',
                        "updated": 'null',
                        "comment": 'null',
                        "maxrisk": 0,
                        "asabusecontact": "anti-spam@ns.chinanet.cn.net",
                        "as": 4812,
                        "asname": "CHINANET-SH-AP China Telecom Group",
                        "ascountry": "CN",
                        "assize": 11671552,
                        "network": "101.80.0.0/13"
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "DShield_Connector",
                "url": "https://isc.sans.edu/ipinfo.html?ip=101.81.5.6"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

dshield_test_transmitQueryData_ip_anoma = {
    "data": [
        {
            "code": 200,
            "data": "101.81.5.6",
            "report": {
                "success": 'true',
                "full": {
                    "threatfeedscount": 0,
                    "ioc_report": {
                        "number": "101.81.5.6",
                        "maxdate": 'null',
                        "mindate": 'null',
                        "updated": 'null',
                        "comment": 'null',
                        "count": 0,
                        "attacks": 0,
                        "maxrisk": 1,
                        "asabusecontact": "anti-spam@ns.chinanet.cn.net",
                        "as": 4812,
                        "asname": "CHINANET-SH-AP China Telecom Group",
                        "ascountry": "CN",
                        "assize": 11671552,
                        "network": "101.80.0.0/13"
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "DShield_Connector",
                "url": "https://isc.sans.edu/ipinfo.html?ip=101.81.5.6"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}