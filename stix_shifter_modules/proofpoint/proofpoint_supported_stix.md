##### Updated on 05/15/23
## Proofpoint (SIEM API)
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
| **x-proofpoint**:threatstatus | threatStatus |
| **x-proofpoint**:threattype | threatType |
| **email-addr**:value | ccAddresses, fromAddress, headerFrom, headerReplyTo, replyToAddress, toAddresses, recipient, sender, headerTo, headerCC |
| **email-message**:cc_refs | ccAddresses, headerCC |
| **email-message**:from_ref | fromAddress, headerFrom, headerReplyTo, replyToAddress |
| **email-message**:to_refs | toAddresses, recipient, headerTo |
| **email-message**:body_multipart | messageParts |
| **email-message**:date | messageTime |
| **email-message**:sender_ref | sender |
| **email-message**:subject | subject |
| **email-message**:is_multipart | is_multipart |
| **ipv4-addr**:value | senderIP, clickIP |
| **ipv6-addr**:value | senderIP, clickIP |
| **network-traffic**:src_ref | senderIP, clickIP |
| **url**:value | threatUrl, url |
| **x-proofpoint-msgevents**:guid | GUID |
| **x-proofpoint-msgevents**:xmailer | xmailer |
| **x-proofpoint-msgevents**:cluster | cluster |
| **x-proofpoint-msgevents**:rewrittenstatus | completelyRewritten |
| **x-proofpoint-msgevents**:impostorscore | impostorScore |
| **x-proofpoint-msgevents**:malwareScore | malwareScore |
| **x-proofpoint-msgevents**:messageid | messageID |
| **x-proofpoint-msgevents**:size | messageSize |
| **x-proofpoint-msgevents**:modulesrun | modulesRun |
| **x-proofpoint-msgevents**:phishscore | phishScore |
| **x-proofpoint-msgevents**:policyroutes | policyRoutes |
| **x-proofpoint-msgevents**:quarantinefolder | quarantineFolder |
| **x-proofpoint-msgevents**:quarantinerule | quarantineRule |
| **x-proofpoint-msgevents**:senderip | senderIP |
| **x-proofpoint-msgevents**:spamscore | spamScore |
| **x-proofpoint-msgevents**:campaignid | campaignID |
| **x-proofpoint-msgevents**:classification | classification |
| **x-proofpoint-msgevents**:threat | threat |
| **x-proofpoint-msgevents**:threatid | threatID |
| **x-proofpoint-msgevents**:threatstatus | threatStatus |
| **x-proofpoint-msgevents**:threattime | threatTime |
| **x-proofpoint-msgevents**:threattype | threatType |
| **x-proofpoint-msgevents**:clicktime | clickTime |
| **x-proofpoint-msgevents**:qid | QID |
| **x-proofpoint-msgevents**:clusterid | clusterId |
| **x-proofpoint-msgevents**:useragent | userAgent |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| email-addr | value | ccAddresses |
| email-addr | value | fromAddress |
| email-addr | value | headerFrom |
| email-addr | value | headerReplyTo |
| email-addr | value | replyToAddress |
| email-addr | value | toAddresses |
| email-addr | value | recipient |
| email-addr | value | sender |
| email-addr | value | headerTo |
| email-addr | value | headerCC |
| <br> | | |
| email-message | cc_refs | ccAddresses |
| email-message | from_ref | fromAddress |
| email-message | from_ref | headerFrom |
| email-message | from_ref | headerReplyTo |
| email-message | from_ref | replyToAddress |
| email-message | to_refs | toAddresses |
| email-message | body_multipart | messageParts |
| email-message | date | messageTime |
| email-message | to_refs | recipient |
| email-message | sender_ref | sender |
| email-message | subject | subject |
| email-message | is_multipart | is_multipart |
| email-message | to_refs | headerTo |
| email-message | cc_refs | headerCC |
| <br> | | |
| ipv4-addr | value | senderIP |
| ipv4-addr | value | clickIP |
| <br> | | |
| ipv6-addr | value | senderIP |
| ipv6-addr | value | clickIP |
| <br> | | |
| network-traffic | src_ref | senderIP |
| network-traffic | src_ref | clickIP |
| <br> | | |
| url | value | threatUrl |
| url | value | url |
| <br> | | |
| x-proofpoint-msgevents | guid | GUID |
| x-proofpoint-msgevents | xmailer | xmailer |
| x-proofpoint-msgevents | cluster | cluster |
| x-proofpoint-msgevents | rewrittenstatus | completelyRewritten |
| x-proofpoint-msgevents | impostorscore | impostorScore |
| x-proofpoint-msgevents | malwarescore | malwareScore |
| x-proofpoint-msgevents | messageid | messageID |
| x-proofpoint-msgevents | size | messageSize |
| x-proofpoint-msgevents | modulesrun | modulesRun |
| x-proofpoint-msgevents | phishscore | phishScore |
| x-proofpoint-msgevents | policyroutes | policyRoutes |
| x-proofpoint-msgevents | quarantinefolder | quarantineFolder |
| x-proofpoint-msgevents | quarantinerule | quarantineRule |
| x-proofpoint-msgevents | senderip | senderIP |
| x-proofpoint-msgevents | spamscore | spamScore |
| x-proofpoint-msgevents | campaignid | campaignID |
| x-proofpoint-msgevents | classification | classification |
| x-proofpoint-msgevents | threat | threat |
| x-proofpoint-msgevents | threatid | threatID |
| x-proofpoint-msgevents | threatstatus | threatStatus |
| x-proofpoint-msgevents | threattime | threatTime |
| x-proofpoint-msgevents | threattype | threatType |
| x-proofpoint-msgevents | clicktime | clickTime |
| x-proofpoint-msgevents | qid | QID |
| x-proofpoint-msgevents | clusterid | clusterId |
| x-proofpoint-msgevents | useragent | userAgent |
| <br> | | |
