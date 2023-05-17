##### Updated on 05/15/23
## Cisco Threat Grid
### Results STIX Domain Objects
* Identity
* Sighting
* Infrastructure
* Malware
* Extension
* Indicator
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
| LIKE | = |
| IN | IN |
| MATCHES | CONTAINS |
| ISSUBSET | insubnet |
| OR (Observation) | OR |
| AND (Observation) | AND |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | SourceIpV4, DestinationIpV4 |
| **ipv6-addr**:value | SourceIpV6, DestinationIpV6 |
| **domain-name**:value | Url |
| **file**:hashes.'SHA-256' | sha256hash |
| **file**:hashes.MD5 | md5hash |
| **file**:hashes.'MD5' | md5hash |
| **file**:hashes.'SHA-1' | sha1hash |
| <br> | |
