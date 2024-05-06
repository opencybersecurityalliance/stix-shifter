### STIX Pattern Use cases and examples

Cisco Secure Email consists of two groups of attributes: Basic attributes and Event attributes. Below examples explain how these 
fields can be used in queries with ‘OR’ and ‘AND’ operators.


| <b>Field Group | <b>STIX Fields |
|------|-----|
| <b>1 - Basic Attributes |
|  'LIKE' operator is supported for string type fields.<br>'AND" and 'OR' operators are supported between basic fields.|  email-addr:value<br>email-message:from_ref<br>email-message:sender_ref<br>email-message:to_refs<br>email-message:subject<br>email-message:x_message_id_header<br>email-message:x_message_id_header<br>email-message:x_sender_ip_ref<br>file:name<br>file:hashes.'SHA-256'<br>ipv4-addr:value<br>ipv6-addr:value<br>domain-name:value<br>x-oca-host:hostname|
Query Example: (Operators between basic attributes)
```[email-addr:value = 'test@xyz.com'] START t'2023-09-14T16:43:00.000Z' STOP t'2023-09-30T16:43:00.000Z'

[email-addr:value = 'test@xyz.com' AND email-message:subject LIKE 'warnings'] START t'2023-09-14T16:43:00.000Z' STOP t'2023-09-30T16:43:00.000Z'

[file:name LIKE 'Microsoft' AND file:hashes.'SHA-256' ='271c0119ac4455fc8db4ef4a8ca8e2bfcfb8bbd3b8c894e117a9ae9f7111111'] START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'

[email-addr:value = 'test@xyz.com' OR email-message:subject LIKE 'warnings'] START t'2023-09-14T16:43:00.000Z' STOP t'2023-09-30T16:43:00.000Z'
```
Expected Result: STIX objects will be returned if data found in data source.
<br>

| <b>Field Group | <b>STIX Fields |
|---------|-----|
| <b>2 - Message Event Attributes | <b>Grouped in x-cisco-email-msgevent |
| ‘OR’ operator is supported between message event fields. <br> ‘AND’ operator is not supported between message event fields. | x-cisco-email-msgevent:advanced_malware_protection_mailflow_direction<br>x-cisco-email-msgevent:advanced_malware_protection<br>x-cisco-email-msgevent:app_forwarding<br>x-cisco-email-msgevent:content_filters_name<br>x-cisco-email-msgevent:content_filters_direction<br>x-cisco-email-msgevent:content_filters_action<br>x-cisco-email-msgevent:dane_failure<br>x-cisco-email-msgevent:message_status<br>x-cisco-email-msgevent:message_delivered<br>x-cisco-email-msgevent:dlp_violations_names<br>x-cisco-email-msgevent:dlpViolationsSeverities<br>x-cisco-email-msgevent:dlp_action<br>x-cisco-email-msgevent:dmarc_from<br>x-cisco-email-msgevent:dmarc_action<br>x-cisco-email-msgevent:etf_sources <br>x-cisco-email-msgevent:etf_iocs <br>x-cisco-email-msgevent:forged_email_detection <br>x-cisco-email-msgevent:geo_location <br>x-cisco-email-msgevent:graymail <br>x-cisco-email-msgevent:hard_bounced <br>x-cisco-email-msgevent:ip_reputation <br>x-cisco-email-msgevent:macro_mailflow_direction <br>x-cisco-email-msgevent:macro_file_types_detected <br>x-cisco-email-msgevent:message_filters <br>x-cisco-email-msgevent:message_direction <br>x-cisco-email-msgevent:contained_malicious_urls <br>x-cisco-email-msgevent:contained_neutral_urls <br>x-cisco-email-msgevent:outbreak_filters_url_rewritten_byof <br>x-cisco-email-msgevent:outbreak_filtersVofThreatCategory <br>x-cisco-email-msgevent:in_outbreak_quarantine <br>x-cisco-email-msgevent:quarantined_to <br>x-cisco-email-msgevent:reply_to <br>x-cisco-email-msgevent:s_mime <br>x-cisco-email-msgevent:domain_categories <br>x-cisco-email-msgevent:sdr_categories <br>x-cisco-email-msgevent:sdr_threat_levels <br>x-cisco-email-msgevent:soft_bounced <br>x-cisco-email-msgevent:spam_positive <br>x-cisco-email-msgevent:quarantined_as_spam <br>x-cisco-email-msgevent:quarantine_status <br>x-cisco-email-msgevent:threat_name <br>x-cisco-email-msgevent:suspect_spam <br>x-cisco-email-msgevent:url_categories <br>x-cisco-email-msgevent:url_reputation <br>x-cisco-email-msgevent:safeprint_ext <br>x-cisco-email-msgevent:virus_positive <br>x-cisco-email-msgevent:web_interaction_tracking_urls <br>x-cisco-email-msgevent:web_interaction_tracking_mailflow_direction <br>x-cisco-email-msgevent:mail_policy <br>x-cisco-email-msgevent:mail_policy_direction|

Query Example:
```
[x-cisco-email-msgevent:spam_positive = 'true' OR x-cisco-email-msgevent:direction = 'incoming'] START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'
```
Expected Result: STIX object matching any of these fields are returned if data found in data source.

Query Example:
```
[x-cisco-email-msgevent:virus_positive = 'true' AND x-cisco-email-msgevent:spam_positive = 'true'] START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z' 
```

Expected Result: Returns error as AND isn’t supported between message attributes
<br><br>

| <b>3 - Basic and Event Attribute: |
|--------------|
| ‘AND’ operator is supported between basic and event fields. <br> ‘OR’ operator is supported between basic and event fields |

Query Example:
```
[email-message:from_ref = 'user1@xyz.com' AND x-cisco-email-msgevent:spam_positive = 'true'] START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z'
```

Expected Result: STIX objects satisfying both the condition are returned if data found in data source.<br><br>Query Example: <br>

```
[ipv4-addr:value = '1.1.1.1' OR x-cisco-email-msgevent:message_status = 'DELIVERED']START t'2023-07-19T01:56:00.000Z' STOP t'2023-09-01T01:57:00.003Z' 
```
Expected Result: STIX object satisfying any of the above condition is returned if data found in data source.
<br>
<br>

| <b>Field Group | <b>STIX Fields |
|---------|-----|
| <b>4 - Event Attributes | <b>Dependent Fields:|
| These event fields will work only when given in combination.| \[content_filters_name, content_filters_direction, content_filters_action] <br><br>\[advanced_malware_protection_mailflow_direction, advanced_malware_protection] <br><br>\[macro_mailflow_directiony, macro_file_types_detected] <br><br>\[web_interaction_tracking_urls, web_interaction_tracking_mailflow_direction] <br><br>\[mail_policy, mail_policy_direction]  |
Query Example:
```
[x-cisco-email-msgevent:content_filters_name = 'test' AND x-cisco-email-msgevent:content_filters_direction = 'inbound' AND x-cisco-email-msgevent:content_filters_action = 'stopped'] START t'2023-08-01T16:43:26.000Z' STOP t'2023-08-30T16:43:26.003Z'
```
Expected Result: STIX objects returned if data found in data source.

Query Example: 
```
[x-cisco-email-msgevent:content_filters_name = 'test' AND x-cisco-email-msgevent:content_filters_direction = 'inbound'] START t'2023-08-01T16:43:26.000Z' STOP t'2023-08-30T16:43:26.003Z'
```
Expected Result: Returns Error as all the required combination fields aren’t given.
<br>
<br>

| <b>Field Group | <b>STIX Fields |
|---------|-----|
| <b>5 - Event Attributes | <b>Enum Supported:||
| ‘IN’ operator is supported for the fields which can have more than one value. |message_status: \[DELIVERED, DROPPED, ABORTED, BOUNCED]<br><br>app_forwarding: \[app_success, app_failed] <br><br>dlpViolationsSeverities: \[critical, high, medium, low] <br><br>x-oca-host:hostname: \[All_Hosts] <br><br>dlp_action: \[delivered, encrypted, dropped] <br><br>dmarc_action: \[none, quarantine, reject, passed, failed] <br><br>etf_iocs: \[file_hash, url, domain] <br><br>s_mime: \[smime_successful, smime_failed] <br><br>quarantine_status: \[POLICY, AMP, AV, UNCLASSIFIED, DLP, OUTBREAK] <br><br>content_filters_direction: \[inbound, outbound] <br><br>content_filters_action: \[stopped] <br><br>advanced_malware_protection_ailflow_direction: \[incoming, outgoing] <br><br>advanced_malware_protection: \[amp_clean, amp_malicious, amp_unknown, amp_unscannable, amp_lowrisk] <br><br>macro_mailflow_direction: \[inbound, outbound] <br><br>web_interaction_tracking_mailflow_direction: \[inbound, outbound] <br><br>mail_policy_direction: \[inbound, outbound]|
Query Example: 
```
[x-cisco-email-msgevent:message_status = 'DELIVERED' ] START t'2023-08-01T16:43:26.000Z' STOP t'2023-08-30T16:43:26.003Z'
 ```
Expected Result: STIX objects returned if data found in data source. 

Query Example: 
```
[x-cisco-email-msgevent:content_filters_direction IN ('inbound', 'outbound') START t'2023-05-19T01:56:00.000Z' STOP t'2023-10-01T01:57:00.003Z'
```
Expected Result: STIX objects returned if data found in data source.






