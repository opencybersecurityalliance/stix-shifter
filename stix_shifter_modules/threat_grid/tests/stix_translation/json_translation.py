threat_grid_ip_value = "193.27.228.59"  #benign
threat_grid_query_pattern = "[ipv4-addr:value='"+threat_grid_ip_value+"']"

threat_grid_domain_value = "moncleroutlets.com" #unknown
threat_grid_query_pattern_domain = "[domain-name:value='"+threat_grid_domain_value+"']"

threat_grid_hash_value = "16cda323189d8eba4248c0a2f5ad0d8f"  #mal
threat_grid_query_pattern_hash = "[file:hashes.MD5='"+threat_grid_hash_value+"']"

threat_grid_ip_anoma = "83.135.186.208" #anomalous
threat_grid_query_pattern_ip = "[ipv4-addr:value='"+threat_grid_ip_anoma+"']"

threat_grid_transmitQueryData_ip_benign = {
    "data": [
        {
            "code": 200,
            "data": "193.27.228.59",
            "report": {
                "success": 'true',
                "full": {
                   "analysis_report":{
                       "threat":{
                           "threat_score": 22,
                           "suspected_categories":{
                               "banking":0,
                               "pua":0,
                               "anti-analysis":0,
                               "anti-forensics":0,
                               "persistence":0,
                               "weakening":0,
                               "evasion":0
                           }
                       },
                       "metadata":{
                           "malware_desc": {
                           }
                       }
                   },
                   "host":"test",
                   "sample_id":"test"
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "ThreatGrid_Connector",
                "url": "N/A"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

threat_grid_transmitQueryData_ip_benign_num = {
"data": [
        {
            "code": 200,
            "data": "193.27.228.59",
            "report": {
                "success": 'true',
                "full": {
                   "analysis_report":{
                       "threat":{
                           "threat_score": 34,
                           "suspected_categories":{
                               "banking":0,
                               "pua":0,
                               "anti-analysis":0,
                               "anti-forensics":0,
                               "persistence":0,
                               "weakening":0,
                               "evasion":0
                           }
                       }
                   }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "ThreatGrid_Connector",
                "url": "N/A"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

threat_grid_transmitQueryData_hash_mal = {
    "data": [
        {
            "code": 200,
            "data": "16cda323189d8eba4248c0a2f5ad0d8f",
            "report": {
                "success": 'true',
                "full": {
                   "analysis_report":{
                       "threat":{
                           "threat_score": 95,
                           "suspected_categories":{
                               "banking":0,
                               "pua":0,
                               "anti-analysis":0,
                               "anti-forensics":0,
                               "persistence":0,
                               "weakening":0,
                               "evasion":0
                           }
                       }
                   }
                }
            },
            "dataType": "hash",
            "external_reference": {
                "source_name": "ThreatGrid_Connector",
                "url": "N/A"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}

threat_grid_transmitQueryData_domain_none = {
"data": [
        {
            "code": 200,
            "data": "moncleroutlets.com",
            "report": {
                "success": 'true',
                "full": {
                    "message": "No sample"
                }
            },
            "dataType": "domain",
            "external_reference": {
                "source_name": "ThreatGrid_Connector",
                "url": "N/A"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
} 

threat_grid_transmitQueryData_ip_anoma = {
    "data": [
        {
            "code": 200,
            "data": "83.135.186.208",
            "report": {
                "success": 'true',
                "full": {
                   "analysis_report":{
                       "threat":{
                           "threat_score": 55,
                           "suspected_categories":{
                               "banking":0,
                               "pua":0,
                               "anti-analysis":0,
                               "anti-forensics":0,
                               "persistence":0,
                               "weakening":0,
                               "evasion":0
                           }
                       }
                   }
                }
            },
            "dataType": "ip",
            "external_reference": {
                "source_name": "ThreatGrid_Connector",
                "url": "N/A"
            },
            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
        }
    ]
}