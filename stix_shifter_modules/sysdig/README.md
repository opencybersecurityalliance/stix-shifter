# Sysdig
## Supported STIX Mappings
See the [table of mappings](sysdig_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**

- [Sysdig API Endpoints](#Sysdig-api-endpoints)
- [Pattern expression with STIX attributes - Single Observation](#Single-observation)
- [Pattern expression with STIX attributes - Multiple Observation](#Multiple-observation)
- [Pattern expression with STIX attributes - Execute Query](#Stix-execute-query)
- [Limitations](#Limitations) 
- [References](#References)


### Sysdig API Endpoints

   | Connector Method | Sysdig API Endpoint                                  | Method |
   |------------------|------------------------------------------------------|--------|
   | Ping Endpoint    | https://< sysdig-server >/api/v1/secureEvents/status | GET    |
   | Events Endpoint  | https://< sysdig-server >/api/v1/secureEvents        | GET    |

### Format for calling stix-shifter from the command line
```
python main.py `<translate or transmit>` `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`
```
### Pattern expression with STIX attributes

### Single Observation

#### STIX Translate query
```shell
translate sysdig query "{}" "[x-sysdig-cluster:name != 'dummycluster'] START t'2023-10-25T16:43:26.000Z' STOP t'2023-11-05T16:43:26.003Z'"
```
#### STIX Translate query - output
```json
{
   "queries": [
        "from=1698252206000000000&to=1699202606003000064&filter=(kubernetes.cluster.name!=\"dummycluster\")andsource!=\"auditTrail\""
   ]   
}
```
#### STIX Transmit query

```shell
transmit
sysdig
"{\"host\": \"dummyhost\", \"port\": 123}"
"{\"auth\": {\"token\": \"abcdefghijklm\"}}"
results
"from=1698252206000000000&to=1699202606003000064&filter=kubernetes.cluster.name!=\"dummycluster\"andsource!=\"auditTrail\""
0
1
```
#### STIX Transmit result - output
```json
{
  "success": true,
  "data": [
    {
      "id": "12345678910",
      "cursor": "ABCDEFGHIJKL",
      "timestamp": "2023-11-01T17:15:14.635115435Z",
      "customerId": 10000,
      "originator": "policy",
      "category": "runtime",
      "source": "syscall",
      "name": "Sysdig Runtime Notable Events",
      "description": "This Notable Events policy contains rules which may indicate undesired behavior including security threats. The rules are more generalized than Threat Detection policies and may result in more noise. Tuning will likely be required for the events generated from this policy.",
      "severity": 30,
      "agentId": 111111,
      "containerId": "1010101010",
      "machineId": "10:10:10:10:10:aa",
      "content": {
        "falsePositive": false,
        "fields": {
          "container.id": "1010101010",
          "container.image.repository": "quay.io/prometheus/node-exporter",
          "container.image.tag": "v1.6.1",
          "container.mounts": "/proc:/host/proc::false:private,/sys:/host/sys::false:private,/:/host/root::false:rslave,/var/lib/kubelet/pods/2f59b128-16ed-4a62-b314-6633e1c85725/etc-hosts:/etc/hosts::true:private,/var/lib/kubelet/pods/2f59b128-16ed-4a62-b314-6633e1c85725/containers/node-exporter/cf6dc919:/dev/termination-log::true:private",
          "container.name": "node-exporter",
          "evt.res": "",
          "evt.type": "event",
          "falco.rule": "Launch Sensitive Mount Container",
          "group.gid": "0",
          "group.name": "",
          "proc.cmdline": "container:1010101010",
          "proc.cwd": "",
          "proc.exepath": "",
          "proc.name": "container:1010101010",
          "proc.pcmdline": "",
          "proc.pid": "-1",
          "proc.ppid": "-1",
          "proc.sid": "-1",
          "user.loginname": "",
          "user.loginuid": "0",
          "user.name": "11111",
          "user.uid": "0", 
          "proc.anames" : []
        },
        "internalRuleName": "Launch Sensitive Mount Container",
        "matchedOnDefault": false,
        "origin": "Sysdig",
        "output": "Container with sensitive mount started (user.name=65534 user.loginuid=0 proc.cmdline=container:8dd62ca5ca80 node-exporter (id=8dd62ca5ca80) image=quay.io/prometheus/node-exporter:v1.6.1 evt.type=container evt.res=<NA> proc.pid=-1 proc.cwd= proc.ppid=-1 proc.pcmdline=<NA> proc.sid=-1 proc.exepath= user.uid=0 user.loginname= group.gid=0 group.name= container.id=8dd62ca5ca80 container.name=node-exporter mounts=/proc:/host/proc::false:private,/sys:/host/sys::false:private,/:/host/root::false:rslave,/var/lib/kubelet/pods/2f59b128-16ed-4a62-b314-6633e1c85725/etc-hosts:/etc/hosts::true:private,/var/lib/kubelet/pods/2f59b128-16ed-4a62-b314-6633e1c85725/containers/node-exporter/cf6dc919:/dev/termination-log::true:private)",
        "policyId": 111000,
        "ruleName": "Launch Sensitive Mount Container",
        "ruleSubType": 0,
        "ruleTags": [
          "container",
          "SOC2",
          "SOC2_CC6.1",
          "NIST",
          "NIST_800-190",
          "NIST_800-190_3.4.3",
          "NIST_800-190_3.5.5",
          "NIST_800-53",
          "NIST_800-53_AC-6(9)",
          "NIST_800-53_AC-6(10)",
          "NIST_800-53_AU-6(8)",
          "ISO",
          "ISO_27001",
          "ISO_27001_A.9.2.3",
          "HIPAA",
          "HIPAA_164.308(a)",
          "HIPAA_164.312(a)",
          "HIPAA_164.312(b)",
          "HITRUST",
          "HITRUST_CSF",
          "HITRUST_CSF_01.c",
          "HITRUST_CSF_09.aa",
          "GDPR",
          "GDPR_32.1",
          "GDPR_32.2",
          "MITRE",
          "MITRE_T1609_container_administration_command",
          "MITRE_T1611_escape_to_host",
          "MITRE_TA0002_execution",
          "MITRE_TA0004_privilege_escalation",
          "MITRE_TA0008_lateral_movement",
          "MITRE_T1610_deploy_container",
          "MITRE_TA0005_defense_evasion",
          "MITRE_T1055.009_process_injection_proc_memory",
          "MITRE_T1543_create_or_modify_system_process",
          "CIS"
        ],
        "ruleType": 6
      },
      "labels": {
        "aws.accountId": "1111111111111",
        "aws.instanceId": "i-101010101010",
        "aws.region": "us-east-1",
        "cloudProvider.account.id": "1111111111111",
        "cloudProvider.name": "aws",
        "cloudProvider.region": "us-east-1",
        "container.image.digest": "sha256:12345678910",
        "container.image.id": "12345",
        "container.image.repo": "quay.io",
        "container.image.tag": "v1.6",
        "container.label.io.kubernetes.container.name": "node-exporter",
        "container.label.io.kubernetes.pod.name": "prometheus-prometheus-node",
        "container.label.io.kubernetes.pod.namespace": "prometheus-monitor",
        "container.name": "node-exporter",
        "host.hostName": "ip-111-111-11-11.ec2.internal",
        "host.mac": "11:11:11:11:11:bb",
        "kubernetes.cluster.name": "cluster",
        "kubernetes.daemonSet.name": "prometheus-prometheus-node",
        "kubernetes.namespace.name": "prometheus-monitor",
        "kubernetes.node.name": "ip-111-111-11-11.ec2.internal",
        "kubernetes.pod.name": "prometheus-prometheus-node-exporter",
        "kubernetes.service.name": "prometheus-prometheus-node-exporter",
        "kubernetes.workload.name": "prometheus-prometheus-node-exporter",
        "kubernetes.workload.type": "daemonset"
      },
      "finding_type": "threat"
    }
  ]
} 

```

#### STIX Translate results

```shell
#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--763ec5eb-efb3-4c96-a96e-3a7bc3fb894b",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sysdig",
            "identity_class": "events",
            "created": "2023-08-01T06:06:52.305Z",
            "modified": "2023-08-02T06:06:52.305Z"
        },
        {
            "id": "observed-data--e91df7cd-1afe-4bf7-96ea-605f1f5a2a69",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-11-29T13:44:13.038Z",
            "modified": "2023-11-29T13:44:13.038Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "x_threat_originator": "policy",
                    "x_category": "runtime",
                    "x_threat_source": "syscall",
                    "x_policy_ref": "1",
                    "severity": 50,
                    "x_agent_id": 111111,
                    "name": "Launch Sensitive Mount Container",
                    "x_cluster_ref": "10",
                    "x_workload_name": "prometheus-prometheus-node-exporter",
                    "x_workload_type": "daemonset",
                    "finding_type": "threat"
                },
                "1": {
                    "type": "x-sysdig-policy",
                    "description": "This Notable Events policy contains rules which may indicate undesired behavior including security threats. The rules are more generalized than Threat Detection policies and may result in more noise. Tuning will likely be required for the events generated from this policy.",
                    "policy_id": 111000,
                    "rule_name": "Launch Sensitive Mount Container",
                    "rule_subtype": 0,
                    "rule_type": 6
                },
                "2": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-container-ext": {
                            "container_id": "1010101010",
                            "x_digest": "sha256:12345678910",
                            "image_id": "12345",
                            "x_repo": "quay.io",
                            "x_tag": "v1.6",
                            "name": "node-exporter"
                        },
                        "x-oca-pod-ext": {
                            "pod_name": "prometheus-prometheus-node"
                            "x_namespace": "prometheus-monitor"
                        }
                    },
                    "hostname": "ip-111-111-11-11.ec2.internal",
                    "mac_refs": [
                        "9"
                    ]
                },
                "3": {
                    "type": "process",
                    "command_line": "container:1010101010",
                    "name": "container:1010101010",
                    "binary_ref": "4",
                    "pid": -1,
                    "x_sid": "-1",
                    "creator_user_ref": "6"
                },
                "4": {
                    "type": "file",
                    "name": "container:1010101010"
                },
                "5": {
                    "type": "process",
                    "pid": -1
                },
                "6": {
                    "type": "user-account",
                    "x_loginuid": "0",
                    "display_name": "11111",
                    "user_id": "0"
                },
                "7": {
                    "type": "x-cloud-provider",
                    "account_id": "1111111111111",
                    "region": "us-east-1",
                    "name": "aws"
                },
                "8": {
                    "type": "x-cloud-resource",
                    "aws_instance_id": "i-101010101010"
                },
                "9": {
                    "type": "mac-addr",
                    "value": "11:11:11:11:11:bb"
                },
                "10": {
                    "type": "x-sysdig-cluster",
                    "name": "cluster",
                    "x_node_ref": "2",
                    "daemonset": "prometheus-prometheus-node",
                    "namespace": "prometheus-monitor"
                }
            },
            "first_observed": "2023-11-01T17:15:14.635115435Z",
            "last_observed": "2023-11-01T17:15:14.635115435Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

### Multiple Observation  with same timestamp

#### STIX Translate query
```shell
translate
sysdig
query
"{}"
"([x-ibm-finding:name = 'contact EC2'] AND [x-sysdig-deployment:name = 'dummydeployment'])START t'2023-10-26T11:00:00.000Z' STOP t'2023-11-07T11:00:00.003Z'"

```

#### STIX Translate query - output

```json
{
     "queries": [
        "from=1700478000000000000&to=1700823600003000064&filter=(ruleName=\"Contact EC2\" or kubernetes.deployment.name=\"dummydeployment\")andsource!=\"auditTrail\""
     ]
}
```

#### STIX Transmit results 

```shell
transmit
sysdig
"{\"host\": \"dummyhost\", \"port\": 123}"
"{\"auth\": {\"token\": \"abcdefghijklm\"}}"
results
"from=1700478000000000000&to=1700823600003000064filter=(ruleName=\"Contact EC2\" or kubernetes.deployment.name=\"dummydeployment\")andsource!=\"auditTrail\""
0
1


```

#### STIX Transmit results - output
```json
{
  "success": true,
  "data": [
    {
      "id": "12345678910",
      "cursor": "ABCDEFGHIJKLMN",
      "timestamp": "2023-11-22T11:16:28.101680299Z",
      "customerId": 10101010,
      "originator": "policy",
      "category": "runtime",
      "source": "syscall",
      "name": "sysdig custom",
      "description": "updated network rules with network tag",
      "severity": 60,
      "agentId": 111111,
      "containerId": "1010101010",
      "machineId": "11:11:1b:11:11:11",
      "content": {
        "falsePositive": false,
        "fields": {
          "container.id": "1010101010",
          "container.image.repository": "docker.io",
          "container.image.tag": "curl",
          "container.name": "curl-sample-app1",
          "evt.res": "EINPROGRESS",
          "evt.type": "connect",
          "falco.rule": "Contact EC2",
          "fd.name": "111.111.11.111:10000->101.101.101.101:10",
          "group.gid": "0",
          "group.name": "root",
          "proc.aname[2]": "containerd-shim",
          "proc.aname[3]": "systemd",
          "proc.aname[4]": "",
          "proc.args": "-s http://101.101.101.101:10/iam/security-credentials",
          "proc.cmdline": "curl -s http://101.101.101.101:10/iam/security-credentials",
          "proc.cwd": "/",
          "proc.exepath": "/usr/bin/curl",
          "proc.name": "curl",
          "proc.pcmdline": "sh",
          "proc.pid": "12345",
          "proc.pname": "sh",
          "proc.ppid": "11111",
          "proc.sid": "1",
          "user.loginname": "",
          "user.loginuid": "-1",
          "user.name": "root",
          "user.uid": "0", 
          "proc.anames": [
            "containerd-shim",
            "systemd"
          ]
        },
        "internalRuleName": "Contact",
        "matchedOnDefault": false,
        "origin": "Secure UI",
        "output": "Outbound connection  (proc.cmdline=curl -s http://101.101.101.101:10/iam/security-credentials proc.name=curl proc.args=-s http://101.101.101.101:10/iam/security-credentials proc.pname=sh gparent=containerd-shim ggparent=systemd gggparent=<NA> connection=111.111.11.111:10000->101.101.101.101:10 curl-sample-app1 (id=10101010) evt.type=connect evt.res=EINPROGRESS proc.pid=12345 proc.cwd=/ proc.ppid=11111 proc.pcmdline=sh proc.sid=1 proc.exepath=/usr/bin/curl user.uid=0 user.loginuid=-1 user.loginname=<NA> user.name=root group.gid=0 group.name=root container.id=1010101010 container.name=curl-sample-app1 image=docker.io/radial/busyboxplus:curl)",
        "policyId": 100100,
        "ruleName": "Contact EC2",
        "ruleSubType": 0,
        "ruleTags": [
          "container",
          "network",
          "aws",
          "SOC2",
          "SOC2_CC6.8",
          "SOC2_CC6.1",
          "NIST",
          "NIST_800-171",
          "NIST_800-171_3.1.1",
          "NIST_800-171_3.1.2",
          "NIST_800-171_3.1.3",
          "NIST_800-171_3.14.6",
          "NIST_800-171_3.14.7",
          "NIST_800-171_3.4.6",
          "NIST_800-53",
          "NIST_800-53_AC-4",
          "NIST_800-53_AC-17",
          "NIST_800-53_SI-4(18)",
          "NIST_800-53_SI-4",
          "NIST_800-53_CM-7",
          "FedRAMP",
          "FedRAMP_CM-7",
          "ISO",
          "ISO_27001",
          "ISO_27001_A.9.1.2",
          "HIPAA",
          "HIPAA_164.308(a)",
          "HIPAA_164.310(b)",
          "HITRUST",
          "HITRUST_CSF",
          "HITRUST_CSF_01.c",
          "HITRUST_CSF_01.i",
          "HITRUST_CSF_01.j",
          "HITRUST_CSF_01.l",
          "HITRUST_CSF_01.n",
          "HITRUST_CSF_01.x",
          "HITRUST_CSF_01.y",
          "HITRUST_CSF_09.ab",
          "HITRUST_CSF_09.ac",
          "HITRUST_CSF_09.i",
          "HITRUST_CSF_09.m",
          "HITRUST_CSF_09.s",
          "HITRUST_CSF_10.j",
          "HITRUST_CSF_10.m",
          "HITRUST_CSF_11.a",
          "HITRUST_CSF_11.b",
          "GDPR",
          "GDPR_32.1",
          "GDPR_32.2",
          "MITRE",
          "MITRE_T1552_unsecured_credentials",
          "MITRE_T1552.005_unsecured_credentials_cloud_instance_metadata_api",
          "MITRE_TA0006_credential_access",
          "MITRE_TA0007_discovery",
          "MITRE_T1552.007_unsecured_credentials_container_api",
          "MITRE_T1033_system_owner_user_discovery",
          "MITRE_T119_automated-collection",
          "MITRE_TA0009_collection"
        ],
        "ruleType": 6
      },
      "labels": {
        "aws.accountId": "111111111111",
        "aws.instanceId": "i-1111111111",
        "aws.region": "us-east-1",
        "cloudProvider.account.id": "111111111111",
        "cloudProvider.name": "aws",
        "cloudProvider.region": "us-east-1",
        "container.image.digest": "sha256:12345",
        "container.image.id": "10101010",
        "container.image.repo": "docker.io/radial/busyboxplus",
        "container.image.tag": "curl",
        "container.label.io.kubernetes.container.name": "curl-sample-app1",
        "container.label.io.kubernetes.pod.name": "curl-sample-app1",
        "container.label.io.kubernetes.pod.namespace": "default",
        "container.name": "curl-sample-app1",
        "host.hostName": "ip-111-111-11-111.ec2.internal",
        "host.mac": "11:11:11:11:11:11",
        "kubernetes.cluster.name": "sysdig",
        "kubernetes.namespace.name": "default",
        "kubernetes.node.name": "ip-111-111-11-111.ec2.internal",
        "kubernetes.pod.name": "curl-sample-app1",
        "process.name": "curl -s http://101.101.101.101/iam/security-credentials"
      },
      "finding_type": "threat",
      "direction": "out",
      "clientIpv4": "111.111.11.111",
      "clientPort": "10000",
      "serverIpv4": "101.101.101.101",
      "serverPort": "10",
      "l4protocol": "tcp"
    }
  ]
}

```


#### STIX Translate results
```shell
#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--8359298b-52b0-4e63-bea9-d84598cb4b5e",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sysdig",
            "identity_class": "events",
            "created": "2023-08-01T06:06:52.305Z",
            "modified": "2023-08-02T06:06:52.305Z"
        },
        {
            "id": "observed-data--48c2872b-2cdb-4d7e-abe3-345e19e4f078",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-11-30T06:27:46.467Z",
            "modified": "2023-11-30T06:27:46.467Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "x_threat_originator": "policy",
                    "x_category": "runtime",
                    "x_threat_source": "syscall",
                    "x_policy_ref": "1",
                    "severity": 100,
                    "x_agent_id": 111111,
                    "name": "Contact EC2",
                    "x_cluster_ref": "12",
                    "finding_type": "threat"
                },
                "1": {
                    "type": "x-sysdig-policy",
                    "description": "updated network rules with network tag",
                    "policy_id": 100100,
                    "rule_name": "Contact EC2",
                    "rule_subtype": 0,
                    "rule_type": 6
                },
                "2": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-container-ext": {
                            "container_id": "1010101010",
                            "x_digest": "sha256:12345",
                            "image_id": "10101010",
                            "x_repo": "docker.io/radial/busyboxplus",
                            "x_tag": "curl",
                            "name": "curl-sample-app1"
                        },
                        "x-oca-pod-ext": {
                            "pod_name": "curl-sample-app1"
                            "x_namespace": "default"
                        }
                    },
                    "hostname": "ip-111-111-11-111.ec2.internal",
                    "mac_refs": [
                        "11"
                    ]
                },
                "3": {
                    "type": "process",
                    "command_line": "curl -s http://101.101.101.101:10/iam/security-credentials",
                    "cwd": "/",
                    "name": "curl",
                    "binary_ref": "5",
                    "pid": 12345,
                    "parent_ref": "7",
                    "x_sid": "1",
                    "creator_user_ref": "8"
                },
                "4": {
                    "type": "directory",
                    "path": "/usr/bin/curl"
                },
                "5": {
                    "type": "file",
                    "parent_directory_ref": "4",
                    "name": "curl"
                },
                "6": {
                    "type": "file",
                    "name": "sh"
                },
                "7": {
                    "type": "process",
                    "command_line": "sh",
                    "name": "sh",
                    "binary_ref": "6",
                    "pid": 11111,
                    "x_parent_names": [
                       "containerd-shim", 
                       "systemd"
                    ]
                },
                "8": {
                    "type": "user-account",
                    "x_loginuid": "-1",
                    "display_name": "root",
                    "user_id": "0"
                },
                "9": {
                    "type": "x-cloud-provider",
                    "account_id": "111111111111",
                    "region": "us-east-1",
                    "name": "aws"
                },
                "10": {
                    "type": "x-cloud-resource",
                    "aws_instance_id": "i-1111111111"
                },
                "11": {
                    "type": "mac-addr",
                    "value": "11:11:11:11:11:11"
                },
                "12": {
                    "type": "x-sysdig-cluster",
                    "name": "sysdig",
                    "x_node_ref": "2",
                    "namespace": "default"
                },
                "13": {
                    "type": "network-traffic",
                    "src_ref": "14",
                    "src_port": 10000,
                    "dst_ref": "15",
                    "dst_port": 10,
                    "protocols": [
                        "tcp"
                    ]
                },
                "14": {
                    "type": "ipv4-addr",
                    "value": "111.111.11.111"
                },
                "15": {
                    "type": "ipv4-addr",
                    "value": "101.101.101.101"
                }
            },
            "first_observed": "2023-11-22T11:16:28.101680299Z",
            "last_observed": "2023-11-22T11:16:28.101680299Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}


```

### Multiple Observation  with different timestamp

#### STIX Translate query
```shell
translate
sysdig
query
"{}"
"[x-oca-asset:extensions.'x-oca-container-ext'.container_id = '1010101010'] START t'2023-10-20T16:43:26.000Z' STOP t'2023-11-01T16:43:26.003Z' OR [x-cloud-provider:name = 'aws'] START t'2023-11-20T16:43:26.000Z' STOP t'2023-11-25T16:43:26.003Z'"
```

#### STIX Translate query - output

```json
{
   "queries": [
        "from=1697820206000000000&to=1698857006003000064&filter=(containerId=\"1010101010\")andsource!=\"auditTrail\"",
        "from=1700498606000000000&to=1700930606003000064&filter=(cloudProvider.name=\"aws\")andsource!=\"auditTrail\""
    ]
}
```

#### STIX Transmit results 

```shell
transmit
sysdig
"{\"host\": \"dummyhost\", \"port\": 123}"
"{\"auth\": {\"token\": \"abcdefghijklm\"}}"
results
"from=1697820206000000000&to=1698857006003000064&filter=(containerId=\"1010101010\")andsource!=\"auditTrail\""
0
1

transmit
sysdig
"{\"host\": \"dummyhost\", \"port\": 123}"
"{\"auth\": {\"token\": \"abcdefghijklm\"}}"
results
"from=1700498606000000000&to=1700930606003000064&filter=(cloudProvider.name=\"aws\")andsource!=\"auditTrail\""
0
1

```

#### STIX Transmit results - output
```json
{
  "success": true,
  "data": [
        {
            "id": "12345678910",
            "cursor": "ABCDEFGHIJKLM",
            "timestamp": "2023-10-25T04:10:56.471969414Z",
            "customerId": 101010,
            "originator": "policy",
            "category": "runtime",
            "source": "syscall",
            "name": "Sysdig Runtime Notable",
            "description": "This Notable Events policy contains rules which may indicate undesired behavior including security threats.",
            "severity": 60,
            "agentId":11111111,
            "containerId": "1010101010",
            "machineId": "00:00:aa:a0:a0:0a",
            "content": {
                "falsePositive": false,
                "fields": {
                    "container.id": "1010101010",
                    "container.image.repository": "quay.io/openshift-release-dev",
                    "container.image.tag": "",
                    "container.name": "sti-build",
                    "evt.res": "SUCCESS",
                    "evt.type": "execve",
                    "falco.rule": "Launch Package Management Process",
                    "group.gid": "0",
                    "group.name": "root",
                    "proc.aname[2]": "exe",
                    "proc.aname[3]": "openshift-sti-b",
                    "proc.aname[4]": "conmon",
                    "proc.cmdline": "pip /opt/app-root/bin/pip install -r requirements.txt",
                    "proc.cwd": "/opt/app-root/src/",
                    "proc.exepath": "/opt/app-root/bin/pip",
                    "proc.name": "pip",
                    "proc.pcmdline": "assemble /usr/libexec/s2i/assemble",
                    "proc.pid": "100000",
                    "proc.pname": "assemble",
                    "proc.ppid": "101010",
                    "proc.sid": "1000",
                    "user.loginname": "",
                    "user.loginuid": "-1",
                    "user.name": "default",
                    "user.uid": "100",
                    "proc.anames": [
                      "exe",
                      "openshift-sti-b",
                      "conmon"
                    ]
                },
                "internalRuleName": "Launch Package Management",
                "matchedOnDefault": false,
                "origin": "Sysdig",
                "output": "Package management process launched in container (user.name=default user.loginuid=-1 proc.name=pip proc.pname=assemble gparent=exe ggparent=openshift-sti-b gggparent=conmon proc.cmdline=pip /opt/app-root/bin/pip install -r requirements.txt container.id=1010101010 container_name=sti-build evt.type=execve evt.res=SUCCESS proc.pid=100000 proc.cwd=/opt/app-root/src/ proc.ppid=195665 proc.pcmdline=assemble /usr/libexec/s2i/assemble proc.sid=111 proc.exepath=/opt/app-root/bin/pip user.uid=100 user.loginname=<NA> group.gid=0 group.name=root container.name=sti-build image=quay.io)",
                "policyId": 1000000,
                "ruleName": "Launch Package Management Process",
                "ruleSubType": 0,
                "ruleTags": [
                    "container",
                    "process",
                    "SOC2",
                    "SOC2_CC6.1",
                    "NIST",
                    "NIST_800-171",
                    "NIST_800-171_3.14.1",
                    "NIST_800-171_3.14.2",
                    "NIST_800-171_3.14.3",
                    "NIST_800-171_3.14.4",
                    "NIST_800-171_3.14.5",
                    "NIST_800-171_3.14.6",
                    "NIST_800-171_3.14.7",
                    "NIST_800-171_3.4.5",
                    "NIST_800-53",
                    "NIST_800-53_CM-5",
                    "NIST_800-53_SI-7",
                    "NIST_800-53_SI-4",
                    "NIST_800-53_SI-3",
                    "FedRAMP",
                    "FedRAMP_SI-3",
                    "ISO",
                    "ISO_27001",
                    "ISO_27001_A.12.5.1",
                    "ISO_27001_A.12.6.2",
                    "ISO_27001_A.14.2.4",
                    "HIPAA",
                    "HIPAA_164.308(a)",
                    "HIPAA_164.312(c)",
                    "HIPAA_164.312(e)",
                    "HITRUST",
                    "HITRUST_CSF",
                    "HITRUST_CSF_01.x",
                    "HITRUST_CSF_09.ab",
                    "HITRUST_CSF_09.ac",
                    "HITRUST_CSF_09.b",
                    "HITRUST_CSF_09.j",
                    "HITRUST_CSF_09.k",
                    "HITRUST_CSF_09.m",
                    "HITRUST_CSF_10.c",
                    "HITRUST_CSF_10.j",
                    "HITRUST_CSF_10.k",
                    "HITRUST_CSF_11.a",
                    "HITRUST_CSF_11.b",
                    "GDPR",
                    "GDPR_32.1",
                    "GDPR_32.2",
                    "MITRE",
                    "MITRE_T1068_exploitation_for_privilege_escalation",
                    "MITRE_TA0003_persistence",
                    "MITRE_TA0004_privilege_escalation",
                    "MITRE_T1569_system_services",
                    "MITRE_TA0042_resource_development",
                    "MITRE_TA0002_execution",
                    "MITRE_T1608.002_stage_capabilities_upload_tool"
                ],
                "ruleType": 6
            },
            "labels": {
                "container.image.digest": "sha256:12345",
                "container.image.id": "12345",
                "container.image.repo": "quay.io/openshift-release-dev",
                "container.label.io.kubernetes.container.name": "sti-build",
                "container.label.io.kubernetes.pod.name": "django-psql-example",
                "container.label.io.kubernetes.pod.namespace": "sample-app2",
                "container.name": "sti-build",
                "host.hostName": "kube-ck8r6iht033m28pqg7ug-cp4scluster-default-000001cc.iks.ibm",
                "host.mac": "00:a0:00:a0:a0:4a",
                "kubernetes.cluster.name": "cluster2",
                "kubernetes.namespace.name": "sample-app2",
                "kubernetes.node.name": "10.100.10.100",
                "kubernetes.pod.name": "example-1-build",
                "process.name": "pip /opt/app-root/bin/pip install"
            },
            "finding_type": "threat"
        }
    ]
}

```
```json
{
    "success": true,
    "data": [
        {
            "id": "12345678910",
            "cursor": "ABCDEFGHIJKLM",
            "timestamp": "2023-11-25T16:40:29.896484649Z",
            "customerId": 12345,
            "originator": "policy",
            "category": "runtime",
            "source": "syscall",
            "name": "Sysdig Runtime Activity Logs",
            "description": "This policy contains rules which provide a greater insight into general activities occuring on the system. They are very noisy, but useful in threat hunting situations if you are looking for specific actions being taken during runtime. It is not recommended to use this policy for detection purposes unless tuning is enabled.  Additional manual tuning will likely be required.",
            "severity": 70,
            "agentId": 5555555,
            "containerId": "10101010",
            "machineId": "11:aa:1a:1a:1a:1a",
            "content": {
                "falsePositive": false,
                "fields": {
                    "container.id": "10101010",
                    "container.image.repository": "docker.io/curlimages/curl",
                    "container.name": "curl-test1",
                    "evt.arg.uid": "curl_user",
                    "evt.res": "",
                    "evt.type": "setuid",
                    "falco.rule": "Non sudo setuid",
                    "group.gid": "101",
                    "group.name": "curl_group",
                    "proc.aname[2]": "systemd",
                    "proc.aname[3]": "",
                    "proc.aname[4]": "",
                    "proc.cmdline": "entrypoint.sh /entrypoint.sh bash",
                    "proc.cwd": "/home/curl_user/",
                    "proc.exepath": "/entrypoint.sh",
                    "proc.name": "entrypoint.sh",
                    "proc.pcmdline": "containerd-shim -namespace k8s.io -address /run/containerd/containerd.sock",
                    "proc.pid": "111111",
                    "proc.pname": "containerd-shim",
                    "proc.ppid": "000000",
                    "proc.sid": "1",
                    "user.loginname": "",
                    "user.loginuid": "-1",
                    "user.name": "curl_user",
                    "user.uid": "100",
                    "proc.anames": [
                      "systemd"
                    ]
                },
                "internalRuleName": "Non sudo setuid",
                "matchedOnDefault": false,
                "origin": "Sysdig",
                "output": "Unexpected setuid call by non-sudo, non-root program (user.name=curl_user user_loginuid=-1 user.uid=100 proc.name=entrypoint.sh parent=containerd-shim gparent=systemd ggparent=<NA> gggparent=<NA> proc.cmdline=entrypoint.sh /entrypoint.sh bash uid=curl_user container.id=10101010 evt.type=setuid evt.res=<NA> proc.pid=111111 proc.cwd=/home/curl_user/ proc.ppid=000000 proc.pcmdline=containerd-shim -namespace k8s.io -id  -address /run/containerd/containerd.sock proc.sid=1 proc.exepath=/entrypoint.sh user.loginuid=-1 user.loginname=<NA> group.gid=101 group.name=curl_group container.name=curl-test1 image=docker.io/curlimages/curl)",
                "policyId": 100000,
                "ruleName": "Non sudo setuid",
                "ruleSubType": 0,
                "ruleTags": [
                    "host",
                    "container",
                    "users",
                    "SOC2",
                    "SOC2_CC6.1",
                    "NIST",
                    "NIST_800-53",
                    "NIST_800-53_AC-6(9)",
                    "NIST_800-53_AC-6(10)",
                    "NIST_800-53_AU-6(8)",
                    "ISO",
                    "ISO_27001",
                    "ISO_27001_A.9.2.3",
                    "HIPAA",
                    "HIPAA_164.308(a)",
                    "HIPAA_164.312(a)",
                    "HIPAA_164.312(b)",
                    "HITRUST",
                    "HITRUST_CSF",
                    "HITRUST_CSF_01.c",
                    "HITRUST_CSF_09.aa",
                    "GDPR",
                    "GDPR_32.1",
                    "GDPR_32.2",
                    "MITRE",
                    "MITRE_TA0005_defense_evasion",
                    "MITRE_T1548.001_abuse_elevation_control_mechanism_setuid_and_setgid MITRE_TA0004_privilege_escalation",
                    "MITRE_T1222_file_and_directory_permissions_modification",
                    "MITRE_T1222.002_file_and_directory_permissions_modification_linux_and_mac_file_and_directory"
                ],
                "ruleType": 6
            },
            "labels": {
                "aws.accountId": "12345",
                "aws.instanceId": "i-000000000",
                "aws.region": "us-east-1",
                "cloudProvider.account.id": "12345",
                "cloudProvider.name": "aws",
                "cloudProvider.region": "us-east-1",
                "container.image.digest": "sha256:12345",
                "container.image.id": "1111111",
                "container.image.repo": "docker.io/curlimages",
                "container.image.tag": "latest",
                "container.label.io.kubernetes.container.name": "curl-test1",
                "container.label.io.kubernetes.pod.name": "curl-test1",
                "container.label.io.kubernetes.pod.namespace": "default",
                "container.name": "curl-test1",
                "host.hostName": "ip-111-111-11-111.ec2.internal",
                "host.mac": "11:aa:11:1a:1a:1a",
                "kubernetes.cluster.name": "sysdig",
                "kubernetes.namespace.name": "default",
                "kubernetes.node.name": "ip-111-111-11-111.ec2.internal",
                "kubernetes.pod.name": "curl-test1",
                "process.name": "entrypoint.sh /entrypoint.sh bash"
            },
            "finding_type": "threat"
        }
    ]
}
```


#### STIX Translate results
```shell
#### STIX Translate results - output
```json
{
    "type": "bundle",
    "id": "bundle--290b25ca-8c55-4784-8a52-8fdcd7561ae1",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sysdig",
            "identity_class": "events",
            "created": "2023-08-01T06:06:52.305Z",
            "modified": "2023-08-02T06:06:52.305Z"
        },
        {
            "id": "observed-data--93c77df8-384c-458a-bfa4-1bcba273f14d",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-11-30T11:03:35.393Z",
            "modified": "2023-11-30T11:03:35.393Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "x_threat_originator": "policy",
                    "x_category": "runtime",
                    "x_threat_source": "syscall",
                    "x_policy_ref": "1",
                    "severity": 60,
                    "x_agent_id": 11111111,
                    "name": "Launch Package Management Process",
                    "x_cluster_ref": "10",
                    "finding_type": "threat"
                },
                "1": {
                    "type": "x-sysdig-policy",
                    "description": "This Notable Events policy contains rules which may indicate undesired behavior including security threats.",
                    "policy_id": 1000000,
                    "rule_name": "Launch Package Management Process",
                    "rule_subtype": 0,
                    "rule_type": 6
                },
                "2": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-container-ext": {
                            "container_id": "1010101010",
                            "x_digest": "sha256:12345",
                            "image_id": "12345",
                            "x_repo": "quay.io/openshift-release-dev",
                            "name": "sti-build"
                        },
                        "x-oca-pod-ext": {
                            "pod_name": "django-psql-example"
                            "x_namespace": "sample-app2"
                        }
                    },
                    "hostname": "kube-ck8r6iht033m28pqg7ug-cp4scluster-default-000001cc.iks.ibm",
                    "mac_refs": [
                        "9"
                    ],
                    "ip_refs": [
                        "11"
                    ]
                },
                "3": {
                    "type": "process",
                    "command_line": "pip /opt/app-root/bin/pip install -r requirements.txt",
                    "cwd": "/opt/app-root/src/",
                    "name": "pip",
                    "binary_ref": "5",
                    "pid": 100000,
                    "parent_ref": "7",
                    "x_sid": "1000",
                    "creator_user_ref": "8"
                },
                "4": {
                    "type": "directory",
                    "path": "/opt/app-root/bin/pip"
                },
                "5": {
                    "type": "file",
                    "parent_directory_ref": "4",
                    "name": "pip"
                },
                "6": {
                    "type": "file",
                    "name": "assemble"
                },
                "7": {
                    "type": "process",
                    "command_line": "assemble /usr/libexec/s2i/assemble",
                    "name": "assemble",
                    "binary_ref": "6",
                    "pid": 101010,
                    "x_parent_names": [
                       "exe",
                       "openshift-sti-b",
                       "conmon"
                    ]
                },
                "8": {
                    "type": "user-account",
                    "x_loginuid": "-1",
                    "display_name": "default",
                    "user_id": "100"
                },
                "9": {
                    "type": "mac-addr",
                    "value": "00:a0:00:a0:a0:4a"
                },
                "10": {
                    "type": "x-sysdig-cluster",
                    "name": "cluster2",
                    "x_node_ref": "2",
                    "namespace": "sample-app2"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "10.100.10.100"
                }
            },
            "first_observed": "2023-10-25T04:10:56.471969414Z",
            "last_observed": "2023-10-25T04:10:56.471969414Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```

```json
{
    "type": "bundle",
    "id": "bundle--de03b315-0a87-4d67-8154-c808f64b87bc",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sysdig",
            "identity_class": "events",
            "created": "2023-08-01T06:06:52.305Z",
            "modified": "2023-08-02T06:06:52.305Z"
        },
        {
            "id": "observed-data--8ab06af8-f8ba-4574-b3c6-e5997430b65a",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-11-30T11:14:05.203Z",
            "modified": "2023-11-30T11:14:05.203Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "x_threat_originator": "policy",
                    "x_category": "runtime",
                    "x_threat_source": "syscall",
                    "x_policy_ref": "1",
                    "severity": 30,
                    "x_agent_id": 5555555,
                    "name": "Non sudo setuid",
                    "x_cluster_ref": "12",
                    "finding_type": "threat"
                },
                "1": {
                    "type": "x-sysdig-policy",
                    "description": "This policy contains rules which provide a greater insight into general activities occuring on the system. They are very noisy, but useful in threat hunting situations if you are looking for specific actions being taken during runtime. It is not recommended to use this policy for detection purposes unless tuning is enabled.  Additional manual tuning will likely be required.",
                    "policy_id": 100000,
                    "rule_name": "Non sudo setuid",
                    "rule_subtype": 0,
                    "rule_type": 6
                },
                "2": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-container-ext": {
                            "container_id": "10101010",
                            "x_digest": "sha256:12345",
                            "image_id": "1111111",
                            "x_repo": "docker.io/curlimages",
                            "x_tag": "latest",
                            "name": "curl-test1"
                        },
                        "x-oca-pod-ext": {
                            "pod_name": "curl-test1",
                            "x_namespace": "default"
                        }
                    },
                    "hostname": "ip-111-111-11-111.ec2.internal",
                    "mac_refs": [
                        "11"
                    ]
                },
                "3": {
                    "type": "process",
                    "command_line": "entrypoint.sh /entrypoint.sh bash",
                    "cwd": "/home/curl_user/",
                    "name": "entrypoint.sh",
                    "binary_ref": "5",
                    "pid": 111111,
                    "parent_ref": "7",
                    "x_sid": "1",
                    "creator_user_ref": "8"
                },
                "4": {
                    "type": "directory",
                    "path": "/entrypoint.sh"
                },
                "5": {
                    "type": "file",
                    "parent_directory_ref": "4",
                    "name": "entrypoint.sh"
                },
                "6": {
                    "type": "file",
                    "name": "containerd-shim"
                },
                "7": {
                    "type": "process",
                    "command_line": "containerd-shim -namespace k8s.io -address /run/containerd/containerd.sock",
                    "name": "containerd-shim",
                    "binary_ref": "6",
                    "pid": 0,
                    "x_parent_names": [
                       "systemd"
                    ]
                },
                "8": {
                    "type": "user-account",
                    "x_loginuid": "-1",
                    "display_name": "curl_user",
                    "user_id": "100"
                },
                "9": {
                    "type": "x-cloud-provider",
                    "account_id": "12345",
                    "region": "us-east-1",
                    "name": "aws"
                },
                "10": {
                    "type": "x-cloud-resource",
                    "aws_instance_id": "i-000000000"
                },
                "11": {
                    "type": "mac-addr",
                    "value": "11:aa:11:1a:1a:1a"
                },
                "12": {
                    "type": "x-sysdig-cluster",
                    "name": "sysdig",
                    "x_node_ref": "2",
                    "namespace": "default"
                }
            },
            "first_observed": "2023-11-25T16:40:29.896484649Z",
            "last_observed": "2023-11-25T16:40:29.896484649Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}

```


#### STIX Execute query
```shell
execute sysdig sysdig "{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"sysdig\",\"identity_class\":\"events\", \"created\":\"2022-05-22T13:22:50.336Z\",\"modified\":\"2022-05-25T13:22:50.336Z\"}" "{\"host\":\"dummyhost\"}" "{\"auth\":{\"token\":\"abcdefghijkl\"}}" "[x-ibm-finding:severity!=100]START t'2023-10-25T16:43:26.000Z' STOP t'2023-11-05T16:43:26.003Z'"

```

#### STIX Execute query - output
```json
{
    "queries": [
        "from=1698252206000000000&to=1699202606003000064&filter=(severity!=0)andsource!=\"auditTrail\""
    ]
}
```
```json
{
    "type": "bundle",
    "id": "bundle--e0cc0a4d-13f7-4746-bf1c-5448679f68da",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "sysdig",
            "identity_class": "events",
            "created": "2023-04-11T16:11:11.878Z",
            "modified": "2023-11-10T16:11:11.878Z"
        },
        {
            "id": "observed-data--07d7dc18-2103-4ae5-974b-1f2044dd5246",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-11-30T09:50:33.962Z",
            "modified": "2023-11-30T09:50:33.962Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "x_threat_originator": "policy",
                    "x_category": "runtime",
                    "x_threat_source": "syscall",
                    "x_policy_ref": "1",
                    "severity": 30,
                    "x_agent_id": 101010,
                    "name": "Launch Sensitive",
                    "x_cluster_ref": "10",
                    "x_workload_name": "prometheus-prometheus-node",
                    "x_workload_type": "daemonset",
                    "finding_type": "threat"
                },
                "1": {
                    "type": "x-sysdig-policy",
                    "description": "This Notable Events policy contains rules which may indicate undesired behavior including security threats. The rules are more generalized than Threat Detection policies and may result in more noise. Tuning will likely be required for the events generated from this policy.",
                    "policy_id": 111111,
                    "rule_name": "Launch Sensitive",
                    "rule_subtype": 0,
                    "rule_type": 6
                },
                "2": {
                    "type": "x-oca-asset",
                    "extensions": {
                        "x-oca-container-ext": {
                            "container_id": "1111111",
                            "x_digest": "sha256:12345",
                            "image_id": "1000000",
                            "x_repo": "quay.io/prometheus",
                            "x_tag": "v1.6.1",
                            "name": "node-exporter"
                        },
                        "x-oca-pod-ext": {
                           "pod_name": "prometheus-prometheus-node-exporter-52glj", 
                           "x_namespace": "prometheus"
                        }
                    },
                    "hostname": "ip-111-111-11-11.ec2.internal",
                    "mac_refs": [
                        "9"
                    ]
                },
                "3": {
                    "type": "process",
                    "command_line": "container:1111111",
                    "name": "container:11111111",
                    "binary_ref": "4",
                    "pid": -1,
                    "x_sid": "-1",
                    "creator_user_ref": "6"
                },
                "4": {
                    "type": "file",
                    "name": "container:1111111"
                },
                "5": {
                    "type": "process",
                    "pid": -1
                },
                "6": {
                    "type": "user-account",
                    "x_loginuid": "0",
                    "display_name": "12345",
                    "user_id": "0"
                },
                "7": {
                    "type": "x-cloud-provider",
                    "account_id": "12345678910",
                    "region": "us-east-1",
                    "name": "aws"
                },
                "8": {
                    "type": "x-cloud-resource",
                    "aws_instance_id": "i-111111111"
                },
                "9": {
                    "type": "mac-addr",
                    "value": "11:11:11:1f:11:bb"
                },
                "10": {
                    "type": "x-sysdig-cluster",
                    "name": "sysdig-cluster1",
                    "x_node_ref": "2",
                    "daemonset": "prometheus-prometheus-node",
                    "namespace": "prometheus"
                }
            },
            "first_observed": "2023-11-01T17:15:14.635115435Z",
            "last_observed": "2023-11-01T17:15:14.635115435Z",
            "number_observed": 1
        }
    ]
}
```

### Limitations
- Query timestamp range should be upto maximum of 14 days
- Sysdig does not support LIKE, MATCHES operators

### References
- [Sysdig] (https://docs.sysdig.com/en/docs/sysdig-secure/)
- [Sysdig API] (https://<sysdig-server>/secure/swagger.html#tag/Secure-Events)