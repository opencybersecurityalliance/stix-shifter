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

`python3 main.py translate "security_advisor" "results" '{"type": "identity", "id":"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "SecurityAdvisor","identity_class": "events"}' '[{"author_account_id": "c4800b388c224809bb25fd12500862e6","author_email": "saksaini@in.ibm.com", "author_id": "IBMid-5500035EWY", "author_kind":"user", "context_account_id": "c4800b388c224809bb25fd12500862e6","context_resource_name": "mycluster", "context_resource_type": "cluster", "create_time":"2019-10-31T11:15:55.099615Z", "create_timestamp": 1572520555100, "description": "file hashand url", "finding_next_steps_0_title": "file hash and url", "finding_severity": "MEDIUM", "id":"853092", "insertion_timestamp": 1572520555100, "kind": "FINDING", "long_description":"http://5.188.86.29:7000", "message":"fdc3e15d2bc80b092f69f89329ff34b7b828be976e5cbe41e3c5720f7896c140", "name":"c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092", "note_name":"c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution", "provider_id":"kubeHunterIBMCloudRemoteCodeExecutor", "provider_name":"c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor","remediation": " Test Remeidation", "reported_by_id":"kubehunteribmcloud-remote-code-execution", "reported_by_title": "Kubehunter IBMCloudcontrol", "short_description": "Kube hunter Remote Code Executor", "update_time":"2019-10-31T11:15:55.099635Z", "update_timestamp": 1572520555100, "update_week_date":"2019-W44-4"}]'`

Will return the following valid STIX Cyber Observable Object:
```json
{
    "type": "bundle",
    "id": "bundle--79d4fad4-a3bd-45be-b64a-6939cb179060",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "SecurityAdvisor",
            "identity_class": "events"
        },
        {
            "id": "observed-data--ba9c0fd5-6422-495a-af99-5a2738231f45",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2019-11-19T09:09:28.652Z",
            "modified": "2019-11-19T09:09:28.652Z",
            "objects": {
                "0": {
                    "type": "author",
                    "author_account_id": "c4800b388c224809bb25fd12500862e6"
                },
                "1": {
                    "type": "author",
                    "email_id": "saksaini@in.ibm.com"
                },
                "2": {
                    "type": "author",
                    "user_id": "IBMid-5500035EWY"
                }
            },
            "context": {
                "context_resource_name": "mycluster",
                "context_resource_type": "cluster"
            },
            "finding": {
                "description": "file hashand url",
                "finding_next_steps_0_title": "file hash and url",
                "finding_severity": "MEDIUM",
                "id": "853092",
                "long_description": "http://5.188.86.29:7000",
                "message": "fdc3e15d2bc80b092f69f89329ff34b7b828be976e5cbe41e3c5720f7896c140",
                "note_name": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution",
                "remediation": " Test Remeidation",
                "short_description": "Kube hunter Remote Code Executor"
            },
            "author": {
                "name": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092"
            },
            "provider": {
                "provider_id": "kubeHunterIBMCloudRemoteCodeExecutor",
                "provider_name": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor",
                "reported_by_id": "kubehunteribmcloud-remote-code-execution",
                "reported_by_title": "Kubehunter IBMCloudcontrol"
            }
        }
    ]
}                                                                                                    
```
