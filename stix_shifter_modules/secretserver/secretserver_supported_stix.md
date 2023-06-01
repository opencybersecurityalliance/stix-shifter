##### Updated on 05/15/23
## IBM Security Verify Privilege Vault
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
### Searchable STIX objects and properties for Event dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | IpAddress, Server |
| **ipv4-addr**:src_ip | IpAddress |
| **ipv4-addr**:dst_ip | Server |
| **url**:value | url |
| **user-account**:display_name | username |
| **user-account**:user_id | UserId |
| **email-addr**:value | EmailAddress |
| **x-secret**:secret_name | SecretName |
| **x-secret**:username | Unique_Identtification |
| **x-secret**:secret_id | ItemId |
| **x-secret**:server_user_name | Username |
| **x-ibm-finding**:event_name | EventSubject |
| **x-ibm-finding**:description | EventNote |
| **x-ibm-finding**:finding_type | EventDetails |
| **x-ibm-finding**:time_observed | EventTime |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| email-addr | value | EmailAddress |
| <br> | | |
| ipv4-addr | value | IpAddress |
| ipv4-addr | value | Server |
| <br> | | |
| url | value | Url |
| <br> | | |
| user-account | display_name | username |
| user-account | user_id | UserId |
| <br> | | |
| x-ibm-finding | src_ip_ref | IpAddress |
| x-ibm-finding | dst_ip_ref | Server |
| x-ibm-finding | event_name | EventSubject |
| x-ibm-finding | description | EventNote |
| x-ibm-finding | finding_type | EventDetails |
| x-ibm-finding | time_observed | EventTime |
| <br> | | |
| x-secret | secret_name | SecretName |
| x-secret | secret_id | ItemId |
| x-secret | username | Unique_Identtification |
| x-secret | server_user_name | Username |
| <br> | | |
