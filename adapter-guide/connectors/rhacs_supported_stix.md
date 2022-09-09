##### Updated on 21/07/22
## RHACS(StackRox)
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | + |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| = | : |
| != | :! |
| LIKE | :r/ |
| MATCHES | :r/ |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| x-rhacs-cluster | name | Cluster |
| x-rhacs-cluster | id | Cluster ID |
| x-rhacs-cluster | namespace | Namespace |
| <br> | | |
| x-rhacs-deployment | name | Deployment |
| x-rhacs-deployment | isactive | Inactive Deployment |
| <br> | | |
| x-ibm-finding | name | Policy |
| x-ibm-finding | time_observed | Violation Time |
| x-ibm-finding | severity | Severity |
| x-ibm-finding | extensions.'x-rhacs-finding'.categories | Category |
| x-ibm-finding | extensions.'x-rhacs-finding'.lifecycle_stage | Lifecycle Stage |
| x-ibm-finding | extensions.'x-rhacs-finding'.violation_state | Violation State |
| x-ibm-finding | extensions.'x-rhacs-finding'.resource_type | Resource Type |
| <br> | | |

