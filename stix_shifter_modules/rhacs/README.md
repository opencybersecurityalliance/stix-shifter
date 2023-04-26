# Redhat Advanced Cluster Security (RHACS) (Previously StackRox)

## Supported STIX Mappings

See the [table of mappings](rhacs_supported_stix.md) for the STIX objects and operators supported by this connector.

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
   
### Note
- RHACS(StackRox) supports both ca and self-signed certificates. Below given transmit and execute examples are based on self-signed. In case of trusted ca issued server certificate, it is not required to pass sni and self-signed parameter as they are optional.  


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
        "Cluster:\"xxxx\"+Violation Time:>=07/07/2022"
    ]
}
```
#### STIX Transmit ping 

```shell
transmit 
rhacs 
"{\"host\":\"xxxxxx\", \"sni\":\"central.stackrox\",\"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"token\": \"xxxxx\"}}" 
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
"{\"host\":\"xxxxxx\", \"sni\":\"central.stackrox\",\"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"token\": \"xxxxx\"}}"
results
"Cluster:"xxxx"+Violation Time:>=07/07/2022"
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
            "policyName": "Unauthorized Network Flow",
            "policyId": "xxxx",
            "description": "This policy generates a violation for the network flows that fall outside baselines for which \"alert on anomalous violations\" is set.",
            "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
            "disabled": false,
            "categories": [
                "Anomalous Activity"
            ],
            "severity": "xxxx",
            "eventSource": "DEPLOYMENT_EVENT",
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "xxxx",
            "lifecycleStage": "xxxx",
            "clusterId": "xxxx",
            "cluster": "xxxx",
            "namespace": "sample-app1",
            "namespaceId": "xxxx",
            "violationState": "ACTIVE",
            "deployment": "xxxx",
            "deploymentId": "xxxx",
            "inactive": false,
            "firstObserved": "2022-09-07T05:39:00.351493134Z",
            "lastObserved": "2022-09-07T05:39:00.351493134Z",
            "violationMessage": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\".",
            "containerName": "django-psql-persistent",
            "containerImage": {
                "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "sample-app1/django-psql-persistent",
                    "tag": "",
                    "fullName": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-persistent",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 0
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 1234
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
{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"rhacs\",\"identity_class\":\"events\",\"created\":\"2022-07-02T13:22:50.336Z\",\"modified\":\"2022-07-10T13:22:50.336Z\"}
"[{\"findingType\": \"violation\",\"alertId\": \"xxxx\",\"policyName\": \"Unauthorized Network Flow\",\"policyId\": \"xxxx\",\"description\": \"This policy generates a violation for the network flows that fall outside baselines for which \\"alert on anomalous violations\\" is set.\",\"rationale\": \"The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.\",\"remediation\": \"Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.\",\"disabled\": false,\"categories\": [\"Anomalous Activity\"],\"severity\": \"HIGH_SEVERITY\",\"eventSource\": \"DEPLOYMENT_EVENT\",\"sortName\": \"Unauthorized Network Flow\",\"sortLifecycleStage\": \"xxxxx\",\"lifecycleStage\": \"xxxx\",\"clusterId\": \"xxxx\",\"cluster\": \"xxxx\",\"namespace\": \"sample-app1\",\"namespaceId\": \"xxxxx\",\"violationState\": \"ACTIVE\",\"deployment\": \"xxxx\",\"deploymentId\": \"xxxx\",\"inactive\": false,\"firstObserved\": \"2022-09-07T05:39:00.351493134Z\",\"lastObserved\": \"2022-09-07T05:39:00.351493134Z\",\"violationMessage\": \"Unexpected network flow found in deployment. Source name: \\"django-psql-persistent\\". Destination name: \\"postgresql\\". Destination port: \\"00000\\". Protocol: \\"L4_PROTOCOL_TCP\\".\",\"containerName\": \"django-psql-persistent\",\"containerImage\": {\"id\": \"sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b\",\"name\": {\"registry\": \"image-registry.openshift-image-registry.svc:5000\",\"remote\": \"sample-app1/django-psql-persistent\",\"tag\": \"\",\"fullName\": \"image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b\"}},\"networkFlow\": {\"netflow_protocol\": \"L4_PROTOCOL_TCP\",\"netflow_source\": {\"name\": \"django-psql-persistent\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-app1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 0},\"netflow_destination\": {\"name\": \"postgresql\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-app1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 00000}}}]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--82b76db2-8646-4226-a144-fdf798492712",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class": "events",
            "created": "2022-07-02T13:22:50.336Z",
            "modified": "2022-07-10T13:22:50.336Z"
        },
        {
            "id": "observed-data--6dec2a80-46ef-4fbe-89e1-768c461d00b7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-09-07T06:06:52.305Z",
            "modified": "2022-09-07T06:06:52.305Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "policy_ref": "1",
                            "categories": [
                                "Anomalous Activity"
                            ],
                            "lifecycle_stage": "xxxx",
                            "cluster_ref": "2",
                            "violation_state": "ACTIVE",
                            "deployment_ref": "3",
                            "description": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\"."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "xxxx",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-cluster",
                    "cluster_id": "xxxx",
                    "name": "xxxx",
                    "namespace": "sample-app1",
                    "namespace_id": "xxxx"
                },
                "3": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "django-psql-persistent",
                    "deployment_id": "xxxx",
                    "isactive": true,
                    "container_refs": [
                        "4"
                    ]
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "xxxx",
                    "image": {
                        "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "sample-app1/django-psql-persistent",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-persistent",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 1234
                    }
                }
            },
            "first_observed": "2022-09-07T05:39:00.351493134Z",
            "last_observed": "2022-09-07T05:39:00.351493134Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

### Multiple Observation  

#### STIX Translate query
```shell
translate
rhacs
query
'{}'
"([x-rhacs-cluster:name = 'xxxx'] AND [x-ibm-finding:extensions.'x-rhacs-finding'.lifecycle_stage = 'xxxx']) START t'2022-07-07T11:00:00.000Z' STOP t'2022-07-08T11:00:00.003Z'"
```

#### STIX Translate query - output

```json
{
    "queries": [
        "Cluster:\"xxxx\"+Violation Time:>=07/07/2022",
        "Lifecycle Stage:\"xxxx\"+Violation Time:>=07/07/2022"
    ]
}
```

#### STIX Transmit results 

```shell
transmit
rhacs
"{\"host\":\"xxxxxx\", \"sni\":\"central.stackrox\",\"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"token\": \"xxxxx\"}}"
results
"Cluster:"xxxx"+Violation Time:>=07/07/2022"
0
1

transmit
rhacs
"{\"host\":\"xxxxxx\", \"sni\":\"central.stackrox\",\"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"token\": \"xxxxx\"}}"
results
"Lifecycle Stage:"xxxx"+Violation Time:>=07/07/2022"
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
            "alertId": "xxxxx",
            "policyName": "Unauthorized Network Flow",
            "policyId": "xxxx",
            "description": "This policy generates a violation for the network flows that fall outside baselines for which \"alert on anomalous violations\" is set.",
            "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
            "disabled": false,
            "categories": [
                "Anomalous Activity"
            ],
            "severity": "HIGH_SEVERITY",
            "eventSource": "DEPLOYMENT_EVENT",
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "xxxx",
            "lifecycleStage": "xxxx",
            "clusterId": "xxxx",
            "cluster": "xxxx",
            "namespace": "sample-app1",
            "namespaceId": "xxxx",
            "violationState": "ACTIVE",
            "deployment": "xxxx",
            "deploymentId": "xxxx",
            "inactive": false,
            "firstObserved": "2022-09-07T05:39:00.351493134Z",
            "lastObserved": "2022-09-07T05:39:00.351493134Z",
            "violationMessage": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\".",
            "containerName": "django-psql-persistent",
            "containerImage": {
                "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "sample-app1/django-psql-persistent",
                    "tag": "",
                    "fullName": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-persistent",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 0
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 1234
                }
            }
        }
    ]
}

```
```json
{
    "success": true,
    "data": [
        {
            "findingType": "violation",
            "alertId": "xxxx",
            "policyName": "Unauthorized Network Flow",
            "policyId": "xxxxx",
            "description": "This policy generates a violation for the network flows that fall outside baselines for which \"alert on anomalous violations\" is set.",
            "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
            "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
            "disabled": false,
            "categories": [
                "Anomalous Activity"
            ],
            "severity": "HIGH_SEVERITY",
            "eventSource": "DEPLOYMENT_EVENT",
            "sortName": "Unauthorized Network Flow",
            "sortLifecycleStage": "xxxx",
            "lifecycleStage": "xxxx",
            "clusterId": "xxxx",
            "cluster": "xxxx",
            "namespace": "sample-app1",
            "namespaceId": "xxxx",
            "violationState": "ACTIVE",
            "deployment": "django-psql-persistent",
            "deploymentId": "xxxx",
            "inactive": false,
            "firstObserved": "2022-09-07T05:44:30.353625545Z",
            "lastObserved": "2022-09-07T05:44:30.353625545Z",
            "violationMessage": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\".",
            "containerName": "django-psql-persistent",
            "containerImage": {
                "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                "name": {
                    "registry": "image-registry.openshift-image-registry.svc:5000",
                    "remote": "sample-app1/django-psql-persistent",
                    "tag": "",
                    "fullName": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                }
            },
            "networkFlow": {
                "netflow_protocol": "L4_PROTOCOL_TCP",
                "netflow_source": {
                    "name": "django-psql-persistent",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 0
                },
                "netflow_destination": {
                    "name": "postgresql",
                    "entity_type": "DEPLOYMENT",
                    "deployment_namespace": "sample-app1",
                    "deployment_type": "DeploymentConfig",
                    "port": 1234
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
{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"rhacs\",\"identity_class\":\"events\",\"created\":\"2022-07-02T13:22:50.336Z\",\"modified\":\"2022-07-10T13:22:50.336Z\"}
"[{\"findingType\": \"violation\",\"alertId\": \"xxxx\",\"policyName\": \"Unauthorized Network Flow\",\"policyId\": \"xxxx\",\"description\": \"This policy generates a violation for the network flows that fall outside baselines for which \\"alert on anomalous violations\\" is set.\",\"rationale\": \"The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.\",\"remediation\": \"Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.\",\"disabled\": false,\"categories\": [\"Anomalous Activity\"],\"severity\": \"HIGH_SEVERITY\",\"eventSource\": \"DEPLOYMENT_EVENT\",\"sortName\": \"Unauthorized Network Flow\",\"sortLifecycleStage\": \"xxxx\",\"lifecycleStage\": \"xxxx\",\"clusterId\": \"xxxx\",\"cluster\": \"xxxx\",\"namespace\": \"sample-app1\",\"namespaceId\": \"xxxx\",\"violationState\": \"ACTIVE\",\"deployment\": \"django-psql-persistent\",\"deploymentId\": \"xxxx\",\"inactive\": false,\"firstObserved\": \"2022-09-07T05:39:00.351493134Z\",\"lastObserved\": \"2022-09-07T05:39:00.351493134Z\",\"violationMessage\": \"Unexpected network flow found in deployment. Source name: \\"django-psql-persistent\\". Destination name: \\"postgresql\\". Destination port: \\"0000\\". Protocol: \\"L4_PROTOCOL_TCP\\".\",\"containerName\": \"django-psql-persistent\",\"containerImage\": {\"id\": \"sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b\",\"name\": {\"registry\": \"image-registry.openshift-image-registry.svc:5000\",\"remote\": \"sample-app1/django-psql-persistent\",\"tag\": \"\",\"fullName\": \"image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b\"}},\"networkFlow\": {\"netflow_protocol\": \"L4_PROTOCOL_TCP\",\"netflow_source\": {\"name\": \"django-psql-persistent\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-app1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 0},\"netflow_destination\": {\"name\": \"postgresql\",\"entity_type\": \"DEPLOYMENT\",\"deployment_namespace\": \"sample-app1\",\"deployment_type\": \"DeploymentConfig\",\"port\": 0000}}}]"
```

#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--82b76db2-8646-4226-a144-fdf798492712",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class": "events",
            "created": "2022-07-02T13:22:50.336Z",
            "modified": "2022-07-10T13:22:50.336Z"
        },
        {
            "id": "observed-data--6dec2a80-46ef-4fbe-89e1-768c461d00b7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-09-07T06:06:52.305Z",
            "modified": "2022-09-07T06:06:52.305Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "policy_ref": "1",
                            "categories": [
                                "Anomalous Activity"
                            ],
                            "lifecycle_stage": "xxxx",
                            "cluster_ref": "2",
                            "violation_state": "ACTIVE",
                            "deployment_ref": "3",
                            "description": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\"."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "xxxx",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-cluster",
                    "cluster_id": "xxxx",
                    "name": "xxxx",
                    "namespace": "sample-app1",
                    "namespace_id": "xxxx"
                },
                "3": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "xxxx",
                    "deployment_id": "xxxx",
                    "isactive": true,
                    "container_refs": [
                        "4"
                    ]
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "xxxx",
                    "image": {
                        "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "sample-app1/django-psql-persistent",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-persistent",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 1234
                    }
                }
            },
            "first_observed": "2022-09-07T05:39:00.351493134Z",
            "last_observed": "2022-09-07T05:39:00.351493134Z",
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
"{\"host\":\"xxxxxx\", \"sni\":\"central.stackrox\",\"selfSignedCert\":\"-----BEGIN CERTIFICATE-----xxxxx-----END CERTIFICATE-----\"}"
"{\"auth\":{\"token\": \"xxxxx\"}}"
"[x-rhacs-cluster:name = 'xxxx'] START t'2022-07-07T08:43:10.003Z' STOP t'2022-07-08T05:35:10.003Z'"
```

#### STIX Execute query - output
```json
{
    "type": "bundle",
    "id": "bundle--37e4ddd1-7113-45b6-9021-c39e6a057749",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "rhacs",
            "identity_class ": "events"
        },
        {
            "id": "observed-data--d093d259-8453-4fa2-8968-29ce0fc0d768",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-09-07T05:52:24.642Z",
            "modified": "2022-09-07T05:52:24.642Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "finding_type": "violation",
                    "extensions": {
                        "x-rhacs-finding": {
                            "alert_id": "xxxx",
                            "policy_ref": "1",
                            "categories": [
                                "Anomalous Activity"
                            ],
                            "lifecycle_stage": "xxxx",
                            "cluster_ref": "2",
                            "violation_state": "ACTIVE",
                            "deployment_ref": "3",
                            "description": "Unexpected network flow found in deployment. Source name: \"django-psql-persistent\". Destination name: \"postgresql\". Destination port: \"5432\". Protocol: \"L4_PROTOCOL_TCP\"."
                        }
                    },
                    "name": "Unauthorized Network Flow",
                    "severity": 75
                },
                "1": {
                    "type": "x-rhacs-policy",
                    "description": "Unauthorized Network Flow",
                    "policy_id": "xxxx",
                    "rationale": "The network baseline is a list of flows that are allowed, and once it is frozen, any flow outside that is a concern.",
                    "remediation": "Evaluate this network flow. If deemed to be okay, add it to the baseline. If not, investigate further as required.",
                    "disabled": false,
                    "event_source": "DEPLOYMENT_EVENT",
                    "sort_name": "Unauthorized Network Flow",
                    "sort_lifecycle_stage": "xxxx"
                },
                "2": {
                    "type": "x-rhacs-cluster",
                    "cluster_id": "xxxx",
                    "name": "xxxx",
                    "namespace": "sample-app1",
                    "namespace_id": "xxxx"
                },
                "3": {
                    "type": "x-rhacs-deployment",
                    "deployment_name": "django-psql-persistent",
                    "deployment_id": "xxxx",
                    "isactive": true,
                    "container_refs": [
                        "4"
                    ]
                },
                "4": {
                    "type": "x-rhacs-container",
                    "container_name": "django-psql-persistent",
                    "image": {
                        "id": "sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b",
                        "name": {
                            "registry": "image-registry.openshift-image-registry.svc:5000",
                            "remote": "sample-app1/django-psql-persistent",
                            "tag": "",
                            "full_name": "image-registry.openshift-image-registry.svc:5000/sample-app1/django-psql-persistent@sha256:653c06dd11972b2e6e3fb94593fd2c290417d5a631aa79c63cb3de24bc425e6b"
                        }
                    }
                },
                "5": {
                    "type": "x-rhacs-networkflow",
                    "protocol": "L4_PROTOCOL_TCP",
                    "source": {
                        "name": "django-psql-persistent",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 0
                    },
                    "destination": {
                        "name": "postgresql",
                        "entity_type": "DEPLOYMENT",
                        "deployment_namespace": "sample-app1",
                        "deployment_type": "DeploymentConfig",
                        "port": 1234
                    }
                }
            },
            "first_observed": "2022-09-07T05:44:30.353625545Z",
            "last_observed": "2022-09-07T05:44:30.353625545Z",
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