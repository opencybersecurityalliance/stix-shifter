# Security Advisor


## Translating Stix Pattern to Security Advisor Query

```
python3 main.py translate "security_advisor" "query" '{}' "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
```

`{'queries': ["[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"]}`

---------------

## Converting from Security Advisor Findings to STIX Cyber Observable Object

Security Advisor data to Stix mapping is defined in `to_stix_map.json` which is located in the security_advisor module.

This example Security Advisor data :

`python3 main.py translate "security_advisor" "results" '{"type": "identity", "id":"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "SecurityAdvisor","identity_class": "events"}' '[{"author_accountId": "test_id", "author_id": "test_user","author_email": "test@gmail.com", "name":"test_id/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092", "id": "853092","noteName":"test_id/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution","updateTime": "2019-10-31T11:15:55.099635Z", "createTime": "2019-10-31T11:15:55.099615Z", "shortDescription": "Kubehunter Remote Code Executor", "providerId": "kubeHunterIBMCloudRemoteCodeExecutor", "providerName":"test_id/providers/kubeHunterIBMCloudRemoteCodeExecutor", "longDescription":"http://5.188.86.29:7000", "context_accountId": "test_id", "context_resourceName": "mycluster","reportedBy_id": "kubehunteribmcloud-remote-code-execution", "reportedBy_title": "Kubehunter IBMCloud control","finding_severity": "MEDIUM", "finding_certainty": "HIGH" , "occurence_count": 1}]'`

Will return the following valid STIX Cyber Observable Object:
```json
{
    "type": "bundle",
    "id": "bundle--bf8762c9-5e77-4285-b3a8-cd4efe3b9945",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "SecurityAdvisor",
            "identity_class": "events"
        },
        {
            "id": "observed-data--a2577bd6-6a4b-48cd-8103-68f78abe8f32",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2019-11-21T11:22:53.717Z",
            "modified": "2019-11-21T11:22:53.717Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "IBMid-5500035EWY"
                },
                "1": {
                    "type": "email-addr",
                    "value": "saksaini@in.ibm.com"
                }
            },
            "x_author": {
                "author_accountId": "c4800b388c224809bb25fd12500862e6"
            },
            "x_finding": {
                "name": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092",
                "id": "853092",
                "noteName": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution",
                "shortDescription": "Kubehunter Remote Code Executor",
                "longDescription": "http://5.188.86.29:7000",
                "context_accountId": "c4800b388c224809bb25fd12500862e6",
                "context_resourceName": "mycluster",
                "finding_severity": "MEDIUM",
                "finding_certainty": "HIGH"
            },
            "last_observed": "2019-10-31T11:15:55.099635Z",
            "first_observed": "2019-10-31T11:15:55.099615Z",
            "x_provider": {
                "providerId": "kubeHunterIBMCloudRemoteCodeExecutor",
                "providerName": "c4800b388c224809bb25fd12500862e6/providers/kubeHunterIBMCloudRemoteCodeExecutor",
                "reportedBy_id": "kubehunteribmcloud-remote-code-execution",
                "reportedBy_title": "Kubehunter IBMCloud control"
            },
            "number_observed": 1
        }
    ]
}                                                                                        
```
