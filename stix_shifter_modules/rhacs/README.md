# RHACS(StackRox) Connector

**Table of Contents**

- [RHACS API Endpoints](#rhacs-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#stix-execute-query)
- [Limitations](#limitations)
- [References](#references)

### RHACS API Endpoints

   |Connector Method|RHACS API Endpoint| Method
   | ----           |   ------              | -----|
   |Alerts Endpoint  |https://<{fqdn}>v1/alerts?query=xxxx|GET
   |Alert by id Endpoint|https://<{fqdn}>v1/alerts/alertid|GET
   |Ping Endpoint|https://<{fqdn}>v1/ping|GET
   
### Format for calling stix-shifter from the command line
```
python main.py `<translate or transmit>` `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query
```shell
translate rhacs query '{}' "[x-rhacs-cluster:name = 'xxxx'] START t'2022-07-07T11:00:00.000Z' STOP t'2022-07-08T11:00:00.003Z'"
```
#### STIX Translate query - output
```json
{
    "queries": [
        "Cluster:\"xxxx\"%2BViolation Time:>=07/07/2022"
    ]
}
```
#### STIX Transmit ping 

```shell
transmit
rhacs
"{\"host\":\"xxxxx"}"
"{\"auth\":{\"token\": "xxxxxx"}}"
ping
```

#### STIX Transmit ping - output
```json
{
    "success": true
}
```
#### STIX Transmit results 

```shell
transmit
rhacs
"{\"host\":\"xxxxx"}"
"{\"auth\":{\"token\": "xxxxxx"}}"
results
"Cluster:\"xxxx\"%2BViolation Time:>=07/07/2022"
0
1
```

#### STIX Transmit result - output
```json
{
    "success": true,
    "data": [
        {
            "findingType": "violation",
            "alertId": "xxxx",
            "cluster": "xxxx",
            "clusterId": "xxxx",
            "namespace": "sample-project1",
            "namespaceId": "bafd2e2e-782e-4a31-aec0-1b3646e236f6",
            "deployment": "xxxx",
            "deploymentId": "xxxx",
            "lifecycleStage": "RUNTIME",
            "policyName": "Unauthorized Network Flow",
            "policyId": "xxxx",
            "description": "This policy generates a violation for the network flows that fall outside baselines for which 'alert on anomalous violations' is set.",
            "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
            "disabled": false,
            "categories": [
                "Anomalous Activity"
            ],
            "eventSource": "DEPLOYMENT_EVENT",
            "severity": "HIGH_SEVERITY",
            "lastUpdated": null,
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "RUNTIME",
            "violationState": "ACTIVE",
            "firstObserved": "2022-07-08T06:16:56.755642667Z",
            "lastObserved": "2022-07-08T06:16:56.755642667Z",
            "violationMessage": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '111111'. Protocol: 'L4_PROTOCOL_TCP'.",
            "containerName": "postgresql",
            "containerImage": {
                "id": "sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "openshift/postgresql",
                    "tag": "",
                    "full_name": "image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-example",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-project1",
                    "deployment_type": "DeploymentConfig",
                    "port": 11111
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-project1",
                    "deployment_type": "DeploymentConfig",
                    "port": 11111
                }
            }
        }
    ]
}
```

#### STIX Translate results

```shell
translate
rhacs
results
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"rhacs\",\"identity_class\":\"events\",\"created\":\"2022-03-16T13:22:50.336Z\",\"modified\":\"2022-03-16T13:22:50.336Z\"}"
"[{\"findingType\": \"violation\",\"alertId\": \"xxxx\",\"cluster\": \"xxxx\",\"clusterId\": \"xxxx\",\"namespace\": \"sample-project1\",\"namespaceId\": \"xxxx\",\"deployment\": \"xxxx\",\"deploymentId\": \"xxxx\",\"lifecycleStage\": \"RUNTIME\",\"policyName\": \"Unauthorized Network Flow\",\"policyId\": \"xxxx\",\"description\": \"This policy generates a violation for the network flows that fall outside baselines for which 'alert on anomalous violations' is set.\",\"rationale\": \"The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.\",\"remediation\": \"Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.\",\"disabled\": false,\"categories\": [\"Anomalous Activity\"],\"eventSource\": \"DEPLOYMENT_EVENT\",\"severity\": \"HIGH_SEVERITY\",\"lastUpdated\": null,\"sortName\": \"Unauthorized Network Flow\",\"sortLifecycleStage\": \"RUNTIME\",\"violationState\": \"ACTIVE\",\"firstObserved\": \"2022-07-08T06:16:56.755642667Z\",\"lastObserved\": \"2022-07-08T06:16:56.755642667Z\",\"violationMessage\": \"Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '11111'. Protocol: 'L4_PROTOCOL_TCP'.\",\"containerName\": \"postgresql\",\"containerImage\": {\"id\": \"sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985\",\"name\": {\"registry\": \"image-registry.openshift-image-registry.svc:5000\",\"remote\": \"openshift/postgresql\",\"tag\": \"\",\"full_name\": \"image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985\"}},\"networkFlow\": {\"netflow_protocol\": \"L4_PROTOCOL_TCP\",\"netflow_source\": {\"name\": \"django-psql-example\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-project1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 0},\"netflow_destination\": {\"name\": \"postgresql\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-project1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 11111}}}]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--0f1f2ed3-7353-46b5-9720-85924a5e43e5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class": "events",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--637585f2-a062-4c47-bde2-0f3288194a5f",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-07-08T06:37:13.377Z",
            "modified": "2022-07-08T06:37:13.377Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "cluster_ref": "1",
                            "deployment_refs": [
                                "2"
                            ],
                            "lifecycle_stage": "RUNTIME",
                            "policy_refs": [
                                "3"
                            ],
                            "state": "ACTIVE",
                            "violation_message": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '11111'. Protocol: 'L4_PROTOCOL_TCP'."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-cluster",
                    "cluster_name": "xxxx",
                    "cluster_id": "xxxx",
                    "namespace": "sample-project1",
                    "namespace_id": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "xxxx",
                    "deployment_id": "xxxx",
                    "container_refs": [
                        "4"
                    ]
                },
                "3": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "xxxx",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "categories": [
                        "Anomalous Activity"
                    ],
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "RUNTIME"
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "postgresql",
                    "container_image": {
                        "id": "sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "openshift/postgresql",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-example",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 11111
                    }
                }
            },
            "first_observed": "2022-07-08T06:16:56.755642667Z",
            "last_observed": "2022-07-08T06:16:56.755642667Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate rhacs query '{}' "[x-rhacs-cluster:name = 'xxxx'] AND [x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'xxxx'] START t'2022-07-07T11:00:00.000Z' STOP t'2022-07-08T11:00:00.003Z'"      
```

#### STIX Translate query - output

```json
{
    "queries": [
        "Cluster:\"xxxx\"%2BViolation Time:>=07/08/2022",
        "Lifecycle Stage:\"xxxx\"%2BViolation Time:>=07/07/2022"
    ]
}
```

#### STIX Transmit results 

```shell
transmit
rhacs
"{\"host\":\"xxxxx"}"
"{\"auth\":{\"token\": "xxxxxx"}}"
results
"Cluster:\"xxxx\"%2BViolation Time:>=07/08/2022","Lifecycle Stage:\"xxxx\"%2BViolation Time:>=07/07/2022"
0
1
```

#### STIX Transmit results - output
```json
{
    "success": true,
    "data": [
        {
            "findingType": "violation",
            "alertId": "85068e91-84c2-4b11-ab4e-0bd02169e1ec",
            "cluster": "xxxx",
            "clusterId": "xxxx",
            "namespace": "sample-project1",
            "namespaceId": "xxxx",
            "deployment": "xxxx",
            "deploymentId": "xxxx",
            "lifecycleStage": "RUNTIME",
            "policyName": "Unauthorized Network Flow",
            "policyId": "xxxx",
            "description": "This policy generates a violation for the network flows that fall outside baselines for which 'alert on anomalous violations' is set.",
            "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
            "disabled": false,
            "categories": [
                "Anomalous Activity"
            ],
            "eventSource": "DEPLOYMENT_EVENT",
            "severity": "HIGH_SEVERITY",
            "lastUpdated": null,
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "RUNTIME",
            "violationState": "ACTIVE",
            "firstObserved": "2022-07-08T09:04:24.721280694Z",
            "lastObserved": "2022-07-08T09:04:24.721280694Z",
            "violationMessage": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '11111'. Protocol: 'L4_PROTOCOL_TCP'.",
            "containerName": "postgresql",
            "containerImage": {
                "id": "sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "openshift/postgresql",
                    "tag": "",
                    "full_name": "image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-example",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-project1",
                    "deployment_type": "DeploymentConfig",
                    "port": 0
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-project1",
                    "deployment_type": "DeploymentConfig",
                    "port": 111111
                }
            }
        }
    ]
}
```

#### STIX Translate results
```shell
translate
rhacs
results
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"rhacs\",\"identity_class\":\"events\",\"created\":\"2022-03-16T13:22:50.336Z\",\"modified\":\"2022-03-16T13:22:50.336Z\"}"
"[{\"findingType\": \"violation\",\"alertId\": \"xxxx\",\"cluster\": \"xxxx\",\"clusterId\": \"xxxx\",\"namespace\": \"sample-project1\",\"namespaceId\": \"xxxx\",\"deployment\": \"xxxx\",\"deploymentId\": \"xxxx\",\"lifecycleStage\": \"RUNTIME\",\"policyName\": \"Unauthorized Network Flow\",\"policyId\": \"1b74ffdd-8e67-444c-9814-1c23863c8ccb\",\"description\": \"This policy generates a violation for the network flows that fall outside baselines for which 'alert on anomalous violations' is set.\",\"rationale\": \"The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.\",\"remediation\": \"Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.\",\"disabled\": false,\"categories\": [\"Anomalous Activity\"],\"eventSource\": \"DEPLOYMENT_EVENT\",\"severity\": \"HIGH_SEVERITY\",\"lastUpdated\": null,\"sortName\": \"Unauthorized Network Flow\",\"sortLifecycleStage\": \"RUNTIME\",\"violationState\": \"ACTIVE\",\"firstObserved\": \"2022-07-08T09:04:24.721280694Z\",\"lastObserved\": \"2022-07-08T09:04:24.721280694Z\",\"violationMessage\": \"Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '11111'. Protocol: 'L4_PROTOCOL_TCP'.\",\"containerName\": \"postgresql\",\"containerImage\": {\"id\": \"sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985\",\"name\": {\"registry\": \"image-registry.openshift-image-registry.svc:5000\",\"remote\": \"openshift/postgresql\",\"tag\": \"\",\"full_name\": \"image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985\"}},\"networkFlow\": {\"netflow_protocol\": \"L4_PROTOCOL_TCP\",\"netflow_source\": {\"name\": \"django-psql-example\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-project1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 0},\"netflow_destination\": {\"name\": \"postgresql\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-project1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 11111}}}]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--a71ff82b-8d9a-46ee-88cb-c847edd614dc",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class": "events",
            "created": "2022-03-16T13:22:50.336Z",
            "modified": "2022-03-16T13:22:50.336Z"
        },
        {
            "id": "observed-data--e827bddd-1adf-4212-a420-b45ac14f9f4f",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-07-08T09:17:15.629Z",
            "modified": "2022-07-08T09:17:15.629Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "cluster_ref": "1",
                            "deployment_refs": [
                                "2"
                            ],
                            "lifecycle_stage": "RUNTIME",
                            "policy_refs": [
                                "3"
                            ],
                            "state": "ACTIVE",
                            "violation_message": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '11111'. Protocol: 'L4_PROTOCOL_TCP'."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-cluster",
                    "cluster_name": "xxxx",
                    "cluster_id": "xxxx",
                    "namespace": "sample-project1",
                    "namespace_id": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "postgresql",
                    "deployment_id": "xxxx",
                    "container_refs": [
                        "4"
                    ]
                },
                "3": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "xxxx",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "categories": [
                        "Anomalous Activity"
                    ],
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "RUNTIME"
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "postgresql",
                    "container_image": {
                        "id": "sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "openshift/postgresql",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/openshift/postgresql@sha256:e3537a12097946baba447c1e0e00306cca045cfe9e9ff4149334fde4e54d6985"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-example",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 11111
                    }
                }
            },
            "first_observed": "2022-07-08T09:04:24.721280694Z",
            "last_observed": "2022-07-08T09:04:24.721280694Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

#### STIX Execute query
```shell
execute
rhacs
rhacs
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"rhacs\",\"identity_class \":\"events\"}"
"{\"host\":\"xxxxx"}"
"{\"auth\":{\"token\": "xxxxxx"}}"
"[x-rhacs-cluster:name = 'xxxx'] START t'2022-07-07T08:43:10.003Z' STOP t'2022-07-08T05:35:10.003Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--afc13681-9c2e-4991-968f-cbcbe638a7c5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--7f2c2c95-10b4-4e1c-9ce8-28c496879bbb",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-07-08T09:22:57.353Z",
            "modified": "2022-07-08T09:22:57.353Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "cluster_ref": "1",
                            "deployment_refs": [
                                "2"
                            ],
                            "lifecycle_stage": "RUNTIME",
                            "policy_refs": [
                                "3"
                            ],
                            "state": "ACTIVE",
                            "violation_message": "Unexpected network flow found in deployment. Source name: 'django-psql-example'. Destination name: 'postgresql'. Destination port: '111111'. Protocol: 'L4_PROTOCOL_TCP'."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-cluster",
                    "cluster_name": "xxxx",
                    "cluster_id": "xxxx",
                    "namespace": "sample-project1",
                    "namespace_id": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "django-psql-example",
                    "deployment_id": "xxxx",
                    "container_refs": [
                        "4"
                    ]
                },
                "3": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "1b74ffdd-8e67-444c-9814-1c23863c8ccb",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "categories": [
                        "Anomalous Activity"
                    ],
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "RUNTIME"
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "django-psql-example",
                    "container_image": {
                        "id": "sha256:661dbef98c61f07715676dc82da579627ff4571208b6b4c97982d97c8f8abf79",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "sample-project1/django-psql-example",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/sample-project1/django-psql-example@sha256:661dbef98c61f07715676dc82da579627ff4571208b6b4c97982d97c8f8abf79"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-example",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-project1",
                        "deployment_type": "DeploymentConfig",
                        "port": 11111
                    }
                }
            },
            "first_observed": "2022-07-08T09:14:54.708831668Z",
            "last_observed": "2022-07-08T09:14:54.708831668Z",
            "number_observed": 1
        }
        
    ],
    "spec_version": "2.0"
}
```

### Limitations
- RHACS(StackRox) does not support "OR" operator in between two entity.
- RHACS(StackRox) does not support "IN" operator
- Violation Time supports mm/dd/yyyy date format.
- Since start stop qualifier not exposed by rhacs so violation time is considered as start qualifier and query returns record greater than or equal to start qualifier.
- If violation time is passed as a stix pattern then start stop qualifier will not be considered.

### References
- [RHACS(StackRox)](https://docs.openshift.com/acs/3.66/support/getting-support-stackrox.html)