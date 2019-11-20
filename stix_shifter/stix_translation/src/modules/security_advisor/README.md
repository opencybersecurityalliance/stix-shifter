# Security Advisor


## Translating Stix Pattern to Security Advisor Query

```
python3 main.py translate "security_advisor" "query" '{}' "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"
```

`{'queries': [["[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"]]}`

---------------

## Converting from Security Advisor Findings to STIX Cyber Observable Object

Security Advisor data to Stix mapping is defined in `to_stix_map.json` which is located in the security_advisor module.

This example Security Advisor data :

`python3 main.py translate "security_advisor" "results" '{"type": "identity", "id":"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "SecurityAdvisor","identity_class": "events"}' '[{"author_account_id": "fgh678vbn678vbn67vb67","author_email": "saksaini@in.ibm.com", "author_id": "IBMid-5500035EWY", "author_kind":"user", "context_account_id": "fgh678vbn678vbn67vb67","context_resource_name": "mycluster", "context_resource_type": "cluster", "create_time":"2019-10-31T11:15:55.099615Z", "create_timestamp": 1572520555100, "description": "file hashand url", "finding_next_steps_0_title": "file hash and url", "finding_severity": "MEDIUM", "id":"853092", "insertion_timestamp": 1572520555100, "kind": "FINDING", "long_description":"http://5.188.86.29:7000", "message":"fdc3e15d2bc80b092f69f89329ff34b7b828be976e5cbe41e3c5720f7896c140", "name":"fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092", "note_name":"fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution", "provider_id":"kubeHunterIBMCloudRemoteCodeExecutor", "provider_name":"fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor","remediation": " Test Remeidation", "reported_by_id":"kubehunteribmcloud-remote-code-execution", "reported_by_title": "Kubehunter IBMCloudcontrol", "short_description": "Kube hunter Remote Code Executor", "update_time":"2019-10-31T11:15:55.099635Z", "update_timestamp": 1572520555100, "update_week_date":"2019-W44-4"}]'`

Will return the following valid STIX Cyber Observable Object:
```json
{
    "type": "bundle",
    "id": "bundle--9286e826-2357-47ea-b7a8-0431cebc30b5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "SecurityAdvisor",
            "identity_class": "events"
        },
        {
            "id": "observed-data--cc7b4302-c983-4c01-82e7-61bb46a430d4",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2019-11-20T06:08:12.939Z",
            "modified": "2019-11-20T06:08:12.939Z",
            "objects": {
                "0": {
                    "type": "author",
                    "author_account_id": "fgh678vbn678vbn67vb67"
                },
                "1": {
                    "type": "email-addr",
                    "value": "saksaini@in.ibm.com"
                },
                "2": {
                    "type": "user-account",
                    "user_id": "IBMid-5500035EWY"
                }
            },
            "x_finding": {
                "context_resource_name": "mycluster",
                "context_resource_type": "cluster",
                "description": "file hashand url",
                "finding_next_steps_0_title": "file hash and url",
                "finding_severity": "MEDIUM",
                "id": "853092",
                "long_description": "http://5.188.86.29:7000",
                "message": "fdc3e15d2bc80b092f69f89329ff34b7b828be976e5cbe41e3c5720f7896c140",
                "name": "fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092",
                "note_name": "fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution",
                "remediation": " Test Remeidation",
                "short_description": "Kube hunter Remote Code Executor"
            },
            "x_provider": {
                "provider_id": "kubeHunterIBMCloudRemoteCodeExecutor",
                "provider_name": "fgh678vbn678vbn67vb67/providers/kubeHunterIBMCloudRemoteCodeExecutor",
                "reported_by_id": "kubehunteribmcloud-remote-code-execution",
                "reported_by_title": "Kubehunter IBMCloudcontrol"
            }
        }
    ]
}                                                                                                  
```
