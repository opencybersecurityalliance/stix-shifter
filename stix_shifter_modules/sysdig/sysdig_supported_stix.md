##### Updated on 05/23/24
## Sysdig
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | and |
| OR (Comparison) | or |
| = | = |
| != | != |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | in |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **mac-addr**:value | machineId |
| **x-oca-asset**:hostname | host.hostName |
| **x-oca-asset**:extensions.'x-oca-container-ext'.container_id | containerId |
| **x-oca-asset**:extensions.'x-oca-container-ext'.name | container.name |
| **x-oca-asset**:extensions.'x-oca-container-ext'.image_id | container.image.id |
| **x-oca-asset**:extensions.'x-oca-container-ext'.x_repo | container.image.repo |
| **x-oca-asset**:extensions.'x-oca-container-ext'.x_tag | container.image.tag |
| **x-oca-asset**:extensions.'x-oca-container-ext'.x_digest | container.image.digest |
| **x-oca-asset**:extensions.'x-oca-pod-ext'.pod_name | container.label.io.kubernetes.pod.name |
| **x-oca-asset**:extensions.'x-oca-pod-ext'.x_namespace | container.label.io.kubernetes.pod.namespace |
| **x-ibm-finding**:name | ruleName |
| **x-ibm-finding**:severity | severity |
| **x-ibm-finding**:x_category | category |
| **x-ibm-finding**:x_threat_originator | originator |
| **x-ibm-finding**:x_threat_source | source |
| **x-ibm-finding**:x_agent_id | agentId |
| **x-sysdig-cluster**:name | kubernetes.cluster.name |
| **x-sysdig-cluster**:namespace | kubernetes.namespace.name |
| **x-sysdig-deployment**:name | kubernetes.deployment.name |
| **x-sysdig-policy**:rule_name | ruleName |
| **x-sysdig-policy**:rule_type | ruleType |
| **x-sysdig-policy**:rule_subtype | ruleSubType |
| **x-sysdig-policy**:policy_id | policyId |
| **x-cloud-provider**:account_id | aws.accountId |
| **x-cloud-provider**:name | cloudProvider.name |
| **x-cloud-provider**:region | aws.region |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | proc.exepath |
| <br> | | |
| file | name | proc.name |
| file | parent_directory_ref | proc.exepath |
| file | name | proc.pname |
| <br> | | |
| ipv4-addr | value | serverIpv4 |
| ipv4-addr | value | clientIpv4 |
| ipv4-addr | value | kubernetes.node.name |
| <br> | | |
| mac-addr | value | host.mac |
| <br> | | |
| network-traffic | protocols | l4protocol |
| network-traffic | src_port | clientPort |
| network-traffic | dst_port | serverPort |
| network-traffic | dst_ref | serverIpv4 |
| network-traffic | src_ref | clientIpv4 |
| <br> | | |
| process | command_line | proc.cmdline |
| process | name | proc.name |
| process | binary_ref | proc.name |
| process | pid | proc.pid |
| process | x_sid | proc.sid |
| process | cwd | proc.cwd |
| process | name | proc.pname |
| process | parent_ref | proc.pname |
| process | binary_ref | proc.pname |
| process | command_line | proc.pcmdline |
| process | pid | proc.ppid |
| process | x_parent_names | proc.anames |
| process | creator_user_ref | user.name |
| <br> | | |
| user-account | account_login | user.loginname |
| user-account | x_loginuid | user.loginuid |
| user-account | display_name | user.name |
| user-account | user_id | user.uid |
| <br> | | |
| x-cloud-provider | account_id | aws.accountId |
| x-cloud-provider | name | cloudProvider.name |
| x-cloud-provider | region | aws.region |
| <br> | | |
| x-cloud-resource | aws_instance_id | aws.instanceId |
| <br> | | |
| x-ibm-finding | x_category | category |
| x-ibm-finding | x_threat_originator | originator |
| x-ibm-finding | x_threat_source | source |
| x-ibm-finding | x_agent_id | agentId |
| x-ibm-finding | finding_type | finding_type |
| x-ibm-finding | severity | severity |
| x-ibm-finding | x_policy_ref | description |
| x-ibm-finding | name | falco.rule |
| x-ibm-finding | x_cluster_ref | kubernetes.cluster.name |
| x-ibm-finding | x_deployment_ref | kubernetes.deployment.name |
| x-ibm-finding | x_workload_name | kubernetes.workload.name |
| x-ibm-finding | x_workload_type | kubernetes.workload.type |
| <br> | | |
| x-oca-asset | extensions.x-oca-container-ext.container_id | containerId |
| x-oca-asset | hostname | host.hostName |
| x-oca-asset | extensions.x-oca-container-ext.x_digest | container.image.digest |
| x-oca-asset | extensions.x-oca-container-ext.image_id | container.image.id |
| x-oca-asset | extensions.x-oca-container-ext.x_tag | container.image.tag |
| x-oca-asset | extensions.x-oca-container-ext.x_repo | container.image.repo |
| x-oca-asset | extensions.x-oca-pod-ext.pod_name | container.label.io.kubernetes.pod.name |
| x-oca-asset | extensions.x-oca-pod-ext.x_namespace | container.label.io.kubernetes.pod.namespace |
| x-oca-asset | extensions.x-oca-container-ext.name | container.name |
| x-oca-asset | mac_refs | host.mac |
| x-oca-asset | ip_refs | kubernetes.node.name |
| <br> | | |
| x-sysdig-cluster | name | kubernetes.cluster.name |
| x-sysdig-cluster | x_node_ref | kubernetes.cluster.name |
| x-sysdig-cluster | daemonset | kubernetes.daemonSet.name |
| x-sysdig-cluster | namespace | kubernetes.namespace.name |
| <br> | | |
| x-sysdig-deployment | name | kubernetes.deployment.name |
| <br> | | |
| x-sysdig-policy | description | description |
| x-sysdig-policy | rule_name | ruleName |
| x-sysdig-policy | rule_type | ruleType |
| x-sysdig-policy | rule_subtype | ruleSubType |
| x-sysdig-policy | policy_id | policyId |
| <br> | | |
