##### Updated on 09/09/22
## Red Hat Advanced Cluster Security for Kubernetes (StackRox)
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| = | : |
| != | :! |
| LIKE | :r/ |
| MATCHES | :r/ |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| OR | OR |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| process | name | name |
| process | arguments | args |
| process | pid | pid |
| process | cwd | execFilePath |
| process | created | time |
| process | x_unique_id | id |
| process | creator_user_ref | uid |
| process | extensions.x-rhacs-process.pod_id | podId |
| process | extensions.x-rhacs-process.pod_uid | podUid |
| process | extensions.x-rhacs-process.container_name | containerName |
| <br> | | |
| user-account | user_id | uid |
| user-account | extensions.x-rhacs-user-account.gid | gid |
| <br> | | |
| x-ibm-finding | finding_type | findingType |
| x-ibm-finding | name | policyName |
| x-ibm-finding | extensions.x-rhacs-finding.alert_id | alertId |
| x-ibm-finding | extensions.x-rhacs-finding.cluster_ref | cluster |
| x-ibm-finding | extensions.x-rhacs-finding.deployment_ref | deployment |
| x-ibm-finding | extensions.x-rhacs-finding.lifecycle_stage | lifecycleStage |
| x-ibm-finding | extensions.x-rhacs-finding.policy_ref | policyId |
| x-ibm-finding | extensions.x-rhacs-finding.categories | categories |
| x-ibm-finding | severity | severity |
| x-ibm-finding | extensions.x-rhacs-finding.description | violationMessage |
| x-ibm-finding | extensions.x-rhacs-finding.violation_state | violationState |
| <br> | | |
| x-rhacs-cluster | name | cluster |
| x-rhacs-cluster | cluster_id | clusterId |
| x-rhacs-cluster | namespace | namespace |
| x-rhacs-cluster | namespace_id | namespaceId |
| <br> | | |
| x-rhacs-container | process_ref | name |
| x-rhacs-container | container_name | containerName |
| x-rhacs-container | image.id | id |
| x-rhacs-container | image.name.registry | registry |
| x-rhacs-container | image.name.remote | remote |
| x-rhacs-container | image.name.tag | tag |
| x-rhacs-container | image.name.full_name | fullName |
| <br> | | |
| x-rhacs-deployment | deployment_id | deploymentId |
| x-rhacs-deployment | deployment_name | deployment |
| x-rhacs-deployment | container_refs | containerName |
| x-rhacs-deployment | isactive | inactive |
| <br> | | |
| x-rhacs-networkflow | protocol | netflow_protocol |
| x-rhacs-networkflow | source.name | name |
| x-rhacs-networkflow | source.entity_type | entity_type |
| x-rhacs-networkflow | source.deployment_namespace | deployment_namespace |
| x-rhacs-networkflow | source.deployment_type | deployment_type |
| x-rhacs-networkflow | source.port | port |
| x-rhacs-networkflow | destination.name | name |
| x-rhacs-networkflow | destination.entity_type | entity_type |
| x-rhacs-networkflow | destination.deployment_namespace | deployment_namespace |
| x-rhacs-networkflow | destination.deployment_type | deployment_type |
| x-rhacs-networkflow | destination.port | port |
| x-rhacs-networkflow | time | time |
| <br> | | |
| x-rhacs-policy | description | policyName |
| x-rhacs-policy | policy_id | policyId |
| x-rhacs-policy | description | description |
| x-rhacs-policy | rationale | rationale |
| x-rhacs-policy | remediation | remediation |
| x-rhacs-policy | disabled | disabled |
| x-rhacs-policy | event_source | eventSource |
| x-rhacs-policy | last_updated | lastUpdated |
| x-rhacs-policy | sort_name | sortName |
| x-rhacs-policy | sort_lifecycle_stage | sortLifecycleStage |
| <br> | | |
