##### Updated on 05/15/23
## Alertflex
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | LIKE |
| IN | IN |
| MATCHES | LIKE |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | a.dstIp, a.srcIp |
| **network-traffic**:src_port | a.srcPort |
| **network-traffic**:dst_port | a.dstPort |
| **network-traffic**:src_ref | a.srcIp |
| **network-traffic**:dst_ref | a.dstIp |
| **file**:name | a.fileName |
| **file**:hashes.'SHA-256' | a.hashSha256 |
| **file**:hashes.'SHA-1' | a.hashSha1 |
| **file**:hashes.MD5 | a.hashMd5 |
| **process**:name | a.processName |
| **process**:pid | a.processId |
| **user-account**:user_id | a.userName |
| **x_org_alertflex**:agent | a.agentName |
| **x_org_alertflex**:node | a.nodeId |
| **x_org_alertflex**:source | a.alertSource |
| **x_org_alertflex**:type | a.alertType |
| **x_org_alertflex**:id | a.eventId |
| **x_org_alertflex**:severity | a.alertSeverity |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| file | name | file |
| file | hashes.SHA-1 | sha1 |
| file | hashes.SHA-256 | sha256 |
| file | hashes.MD5 | md5 |
| <br> | | |
| ipv4-addr | value | srcip |
| ipv4-addr | value | dstip |
| <br> | | |
| ipv6-addr | value | srcip |
| ipv6-addr | value | dstip |
| <br> | | |
| network-traffic | src_ref | srcip |
| network-traffic | dst_ref | dstip |
| network-traffic | src_port | srcport |
| network-traffic | dst_port | dstport |
| network-traffic | protocols | protocol |
| <br> | | |
| process | name | process |
| <br> | | |
| user-account | user_id | user |
| <br> | | |
| x-org-alertflex | event | event |
| x-org-alertflex | severity | severity |
| x-org-alertflex | category | category |
| x-org-alertflex | description | description |
| x-org-alertflex | info | info |
| x-org-alertflex | agent | agent |
| x-org-alertflex | source | source |
| x-org-alertflex | finding_type | type |
| x-org-alertflex | node | node |
| <br> | | |
