##### Updated on 02/04/22
## Alertflex
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| OR | OR |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | LIKE |
| IN | IN |
| MATCHES | LIKE |
| <br> | |
### Supported STIX Objects and Properties
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
