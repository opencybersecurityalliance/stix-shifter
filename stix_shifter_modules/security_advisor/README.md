# IBM Cloud Security Advisor

## Supported STIX Mappings

See the [table of mappings](security_advisor_supported_stix.md) for the STIX objects and operators supported by this connector.

## Translating Stix Pattern to Security Advisor Query

```
python3 main.py translate "security_advisor" "query" '{}' "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
```

`{'queries': ["[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"]}`

---------------

## Converting from Security Advisor Findings to STIX Cyber Observable Object

Security Advisor data to Stix mapping is defined in `to_stix_map.json` which is located in the security_advisor module.

This example Security Advisor data :

`python3 main.py translate security_advisor results '{"type": "identity", "id":"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "SecurityAdvisor","identity_class": "events"}' '[{"author_accountId": "4263e551d4a9460e8cdaccc06414198b", "author_id": "iam-ServiceId-7b4398db-219e-4174-b4f5-c6e31970c7dc", "author_email": null, "name": "67035ffbd96ead38e7e5bd6bf40f364a/providers/config-advisor/occurrences/datacos-not_in_private_network-crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F67035ffbd96ead38e7e5bd6bf40f364a%3A895aa3a5-905f-4e78-90c9-d7e86d3032e1%3A%3A", "id": "datacos-not_in_private_network-crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F67035ffbd96ead38e7e5bd6bf40f364a%3A895aa3a5-905f-4e78-90c9-d7e86d3032e1%3A%3A", "noteName": "4263e551d4a9460e8cdaccc06414198b/providers/config-advisor/notes/datacos-not_in_private_network", "updateTime": "2020-01-08T18:03:59.825854Z", "createTime": "2020-01-08T18:03:59.825827Z", "shortDescription": "COS bucket is not in a private network", "providerId": "config-advisor", "providerName": "67035ffbd96ead38e7e5bd6bf40f364a/providers/config-advisor", "longDescription": "Bucket is not in a private network", "context_accountId": "67035ffbd96ead38e7e5bd6bf40f364a", "context_region": "us-south", "context_resourceType": "COS bucket", "context_resourceName": "Any", "context_resourceId": null, "context_resourceCrn": "Any", "context_serviceName": "COS service", "context_serviceCrn": "crn:v1:bluemix:public:cloud-object-storage:global:a/67035ffbd96ead38e7e5bd6bf40f364a:895aa3a5-905f-4e78-90c9-d7e86d3032e1::", "reportedBy_id": "appprotection", "reportedBy_title": "Config Advisor", "reportedBy_url": null, "finding_severity": "HIGH", "finding_certainty": "HIGH", "finding_networkConnection": null, "finding_nextSteps_0_title": "Cloud Object Storage Docs", "finding_nextSteps_0_url": "https://cloud.ibm.com/docs/services/cloud-object-storage?topic=cloud-object-storage-setting-a-firewall", "finding_nextSteps_1_title": "Bucket 'sa.67035ffbd96ead38e7e5bd6bf40f364a.telemetric.us-south' of COS-instance 'securityadvisor.67035ffbd96ead38e7e5bd6bf40f364a.instance' is not using private network. Use REST API to set the private network mask for the bucket", "finding_nextSteps_1_url": null, "finding_dataTransferred": null, "occurence_count": 1}]'`

Will return the following valid STIX Cyber Observable Object:
```json
{
    "type": "bundle",
    "id": "bundle--ff8f94e5-7f08-4cc7-94f7-9fc86408a615",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "SecurityAdvisor",
            "identity_class": "events"
        },
        {
            "id": "observed-data--5c3152c8-b1f4-4425-b56c-4ce3f21613fe",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2020-02-13T16:33:56.650Z",
            "modified": "2020-02-13T16:33:56.650Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "iam-ServiceId-7b4398db-219e-4174-b4f5-c6e31970c7dc"
                },
                "1": {
                    "type": "domain-name",
                    "value": "cloud.ibm.com"
                },
                "2": {
                    "type": "url",
                    "value": "https://cloud.ibm.com/docs/services/cloud-object-storage?topic=cloud-object-storage-setting-a-firewall"
                }
            },
            "x_security_advisor_finding": {
                "author_accountId": "4263e551d4a9460e8cdaccc06414198b",
                "name": "67035ffbd96ead38e7e5bd6bf40f364a/providers/config-advisor/occurrences/datacos-not_in_private_network-crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F67035ffbd96ead38e7e5bd6bf40f364a%3A895aa3a5-905f-4e78-90c9-d7e86d3032e1%3A%3A",
                "id": "datacos-not_in_private_network-crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2F67035ffbd96ead38e7e5bd6bf40f364a%3A895aa3a5-905f-4e78-90c9-d7e86d3032e1%3A%3A",
                "noteName": "4263e551d4a9460e8cdaccc06414198b/providers/config-advisor/notes/datacos-not_in_private_network",
                "shortDescription": "COS bucket is not in a private network",
                "providerId": "config-advisor",
                "providerName": "67035ffbd96ead38e7e5bd6bf40f364a/providers/config-advisor",
                "longDescription": "Bucket is not in a private network",
                "context_accountId": "67035ffbd96ead38e7e5bd6bf40f364a",
                "context_resourceName": "Any",
                "reportedBy_id": "appprotection",
                "reportedBy_title": "Config Advisor",
                "finding_severity": "HIGH",
                "finding_certainty": "HIGH"
            },
            "last_observed": "2020-01-08T18:03:59.825854Z",
            "first_observed": "2020-01-08T18:03:59.825827Z",
            "number_observed": 1
        }
    ]
}                                                                                   
```
