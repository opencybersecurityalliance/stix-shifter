##### Updated on 14/09/23
## Cisco Secure Email
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Cisco Secure Email Operator |
|--|--|
| AND (Comparision) | & |
| = | = |
| IN | = |
| LIKE | = |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **email-addr**:value | envelopeRecipientfilterValue, envelopeSenderfilterValue |
| **email-message**:from_ref | envelopeSenderfilterValue |
| **email-message**:sender_ref | envelopeSenderfilterValue |
| **email-message**:to_refs | envelopeRecipientfilterValue |
| **email-message**:subject | subjectfilterValue |
| **email-message**:x_message_id_header | messageIdHeader |
| **email-message**:x_cisco_mid | ciscoMid |
| **email-message**:x_sender_ip_ref | senderIp |
| **file**:name | attachmentNameValue |
| **file**:hashes.'SHA-256' | fileSha256 |
| **ipv4-addr**:value | senderIp |
| **ipv6-addr**:value | senderIp |
| **domain-name**:value | domainNameValue |
| **x-oca-host**:hostname | ciscoHost |
| **x-cisco-email-msgevent**:advanced_malware_protection_mailflow_direction | advancedMalwareProtectionMailflowDirection |
| **x-cisco-email-msgevent**:advanced_malware_protection | advancedMalwareProtection |
| **x-cisco-email-msgevent**:app_forwarding | appForwarding |
| **x-cisco-email-msgevent**:content_filters_name | contentFiltersName |
| **x-cisco-email-msgevent**:content_filters_direction | contentFiltersDirection |
| **x-cisco-email-msgevent**:content_filters_action | contentFiltersAction |
| **x-cisco-email-msgevent**:dane_failure | daneFailure |
| **x-cisco-email-msgevent**:message_status | deliveryStatus |
| **x-cisco-email-msgevent**:message_delivered | message_delivered |
| **x-cisco-email-msgevent**:dlp_violations_names | dlpViolationsNames |
| **x-cisco-email-msgevent**:dlpViolationsSeverities | dlpViolationsSeverities |
| **x-cisco-email-msgevent**:dlp_action | dlpAction |
| **x-cisco-email-msgevent**:dmarc_from | dmarcFrom |
| **x-cisco-email-msgevent**:dmarc_action | dmarcAction |
| **x-cisco-email-msgevent**:etf_sources | etfSources |
| **x-cisco-email-msgevent**:etf_iocs | etfIocs |
| **x-cisco-email-msgevent**:forged_email_detection | forgedEmailDetection |
| **x-cisco-email-msgevent**:geo_location | geoLocation |
| **x-cisco-email-msgevent**:graymail | graymail |
| **x-cisco-email-msgevent**:hard_bounced | hardBounced |
| **x-cisco-email-msgevent**:ip_reputation | ipReputation |
| **x-cisco-email-msgevent**:macro_mailflow_direction | macroMailflowDirection |
| **x-cisco-email-msgevent**:macro_file_types_detected | macroFileTypesDetected |
| **x-cisco-email-msgevent**:message_filters | messageFilters |
| **x-cisco-email-msgevent**:message_direction | messageDirection |
| **x-cisco-email-msgevent**:contained_malicious_urls | containedMaliciousUrls |
| **x-cisco-email-msgevent**:contained_neutral_urls | containedNeutralUrls |
| **x-cisco-email-msgevent**:outbreak_filters_url_rewritten_byof | outbreakFiltersUrlRewrittenByOf |
| **x-cisco-email-msgevent**:outbreak_filtersVofThreatCategory | outbreakFiltersVofThreatCategory |
| **x-cisco-email-msgevent**:in_outbreak_quarantine | inOutbreakQuarantine |
| **x-cisco-email-msgevent**:quarantined_to | quarantinedTo |
| **x-cisco-email-msgevent**:reply_to | replyToValue |
| **x-cisco-email-msgevent**:s_mime | smime |
| **x-cisco-email-msgevent**:domain_categories | domainCategories |
| **x-cisco-email-msgevent**:sdr_categories | sdrCategories |
| **x-cisco-email-msgevent**:sdr_threat_levels | sdrThreatLevels |
| **x-cisco-email-msgevent**:soft_bounced | softBounced |
| **x-cisco-email-msgevent**:spam_positive | spamPositive |
| **x-cisco-email-msgevent**:quarantined_as_spam | quarantinedAsSpam |
| **x-cisco-email-msgevent**:quarantine_status | quarantineStatus |
| **x-cisco-email-msgevent**:threat_name | threatName |
| **x-cisco-email-msgevent**:suspect_spam | suspectSpam |
| **x-cisco-email-msgevent**:url_categories | urlCategories |
| **x-cisco-email-msgevent**:url_reputation | urlReputation |
| **x-cisco-email-msgevent**:safeprint_ext | safeprintExt |
| **x-cisco-email-msgevent**:virus_positive | virusPositive |
| **x-cisco-email-msgevent**:web_interaction_tracking_urls | webInteractionTrackingUrls |
| **x-cisco-email-msgevent**:web_interaction_tracking_mailflow_direction | webInteractionTrackingMailflowDirection |
| **x-cisco-email-msgevent**:mail_policy | mailPolicyName |
| **x-cisco-email-msgevent**:mail_policy_direction | mailPolicyDirection |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| email-addr | value | envelopeRecipientfilterValue |
| email-addr | value | envelopeSenderfilterValue |
| <br> | | |
| email-message | from_ref | envelopeSenderfilterValue |
| email-message | sender_ref | envelopeSenderfilterValue |
| email-message | to_refs | envelopeRecipientfilterValue |
| email-message | subject | subjectfilterValue |
| email-message | x_message_id_header | messageIdHeader |
| email-message | x_cisco_mid | ciscoMid |
| email-message | x_sender_ip_ref | senderIp |
| <br> | | |
| file | name | attachmentNameValue |
| file | hashes.'SHA-256' | fileSha256 |
| <br> | | |
| ipv4-addr | value | senderIp |
| <br> | | |
| ipv6-addr | value | senderIp |
| <br> | | |
| domain-name | value | domainNameValue |
| <br> | | |
| x-oca-host | hostname | ciscoHost |
| <br> | | |
| x-cisco-email-msgevent | advanced_malware_protection_mailflow_direction | advancedMalwareProtectionMailflowDirection |
| x-cisco-email-msgevent | advanced_malware_protection | advancedMalwareProtection |
| x-cisco-email-msgevent | app_forwarding | appForwarding |
| x-cisco-email-msgevent | content_filters_name | contentFiltersName |
| x-cisco-email-msgevent | content_filters_direction | contentFiltersDirection |
| x-cisco-email-msgevent | content_filters_action | contentFiltersAction |
| x-cisco-email-msgevent | dane_failure | daneFailure |
| x-cisco-email-msgevent | message_status | deliveryStatus |
| x-cisco-email-msgevent | message_delivered | message_delivered |
| x-cisco-email-msgevent | dlp_violations_names | dlpViolationsNames |
| x-cisco-email-msgevent | dlpViolationsSeverities | dlpViolationsSeverities |
| x-cisco-email-msgevent | dlp_action | dlpAction |
| x-cisco-email-msgevent | dmarc_from | dmarcFrom |
| x-cisco-email-msgevent | dmarc_action | dmarcAction |
| x-cisco-email-msgevent | etf_sources | etfSources |
| x-cisco-email-msgevent | etf_iocs | etfIocs |
| x-cisco-email-msgevent | forged_email_detection | forgedEmailDetection |
| x-cisco-email-msgevent | geo_location | geoLocation |
| x-cisco-email-msgevent | graymail | graymail |
| x-cisco-email-msgevent | hard_bounced | hardBounced |
| x-cisco-email-msgevent | ip_reputation | ipReputation |
| x-cisco-email-msgevent | macro_mailflow_direction | macroMailflowDirection |
| x-cisco-email-msgevent | macro_file_types_detected | macroFileTypesDetected |
| x-cisco-email-msgevent | message_filters | messageFilters |
| x-cisco-email-msgevent | message_direction | messageDirection |
| x-cisco-email-msgevent | contained_malicious_urls | containedMaliciousUrls |
| x-cisco-email-msgevent | contained_neutral_urls | containedNeutralUrls |
| x-cisco-email-msgevent | outbreak_filters_url_rewritten_byof | outbreakFiltersUrlRewrittenByOf |
| x-cisco-email-msgevent | outbreak_filtersVofThreatCategory | outbreakFiltersVofThreatCategory |
| x-cisco-email-msgevent | in_outbreak_quarantine | inOutbreakQuarantine |
| x-cisco-email-msgevent | quarantined_to | quarantinedTo |
| x-cisco-email-msgevent | reply_to | replyToValue |
| x-cisco-email-msgevent | s_mime | smime |
| x-cisco-email-msgevent | domain_categories | domainCategories |
| x-cisco-email-msgevent | sdr_categories | sdrCategories |
| x-cisco-email-msgevent | sdr_threat_levels | sdrThreatLevels |
| x-cisco-email-msgevent | soft_bounced | softBounced |
| x-cisco-email-msgevent | spam_positive | spamPositive |
| x-cisco-email-msgevent | quarantined_as_spam | quarantinedAsSpam |
| x-cisco-email-msgevent | quarantine_status | quarantineStatus |
| x-cisco-email-msgevent | threat_name | threatName |
| x-cisco-email-msgevent | suspect_spam | suspectSpam |
| x-cisco-email-msgevent | url_categories | urlCategories |
| x-cisco-email-msgevent | url_reputation | urlReputation |
| x-cisco-email-msgevent | safeprint_ext | safeprintExt |
| x-cisco-email-msgevent | virus_positive | virusPositive |
| x-cisco-email-msgevent | web_interaction_tracking_urls | webInteractionTrackingUrls |
| x-cisco-email-msgevent | web_interaction_tracking_mailflow_direction | webInteractionTrackingMailflowDirection |
| x-cisco-email-msgevent | mail_policy | mailPolicyName |
| x-cisco-email-msgevent | mail_policy_direction | mailPolicyDirection |
| <br> | | |
