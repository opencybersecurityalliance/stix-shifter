##### Updated on 02/04/22
## Secret Server
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
| ipv4-addr | value | IpAddress |
| ipv4-addr | value | Server |
| <br> | | |
| url | value | Url |
| <br> | | |
| user-account | user_name | username |
| <br> | | |
| x-ibm-finding | src_ip_ref | IpAddress |
| x-ibm-finding | dst_ip_ref | Server |
| x-ibm-finding | name | EventSubject |
| x-ibm-finding | description | EventNote |
| x-ibm-finding | finding_type | EventDetails |
| x-ibm-finding | time_observed | EventTime |
| <br> | | |
| x-secret | secret_name | SecretName |
| x-secret | secret_id | ItemId |
| x-secret | user_id | UserId |
| <br> | | |
