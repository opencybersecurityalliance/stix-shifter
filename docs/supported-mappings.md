# Currently supported STIX objects and properties

Each connector supports a set of STIX objects and properties as defined in the connector's mapping files. There is also a set of common STIX properties that all cyber observable objects must contain. See [STIX™ Version 2.0. Part 4: Cyber Observable Objects](http://docs.oasis-open.org/cti/stix/v2.0/stix-v2.0-part4-cyber-observable-objects.html) for more information on STIX objects.
## Common cyber observable properties

- created
- modified
- first_observed
- last_observed
- number_observed

## Supported data sources

Stix-shifter currently offers connector support for the following cybersecurity products. Click on a data source to see a list of STIX attributes and properties it supports.

- [Alertflex](../stix_shifter_modules/alertflex/alertflex_supported_stix.md)
- [Micro Focus ArcSight](../stix_shifter_modules/arcsight/arcsight_supported_stix.md)
- [Amazon Athena](../stix_shifter_modules/aws_athena/aws_athena_supported_stix.md)
- [Amazon CloudWatch Logs](../stix_shifter_modules/aws_cloud_watch_logs/aws_cloud_watch_logs_supported_stix.md)
- [Amazon GuardDuty](../stix_shifter_modules/aws_guardduty/aws_guardduty_supported_stix.md)
- [Azure Log Analytics](../stix_shifter_modules/azure_log_analytics/azure_log_analytics_supported_stix.md)
- [Microsoft Graph Security](../stix_shifter_modules/azure_sentinel/azure_sentinel_supported_stix.md)
- [HCL BigFix](../stix_shifter_modules/bigfix/bigfix_supported_stix.md)
- [Carbon Black CB Response](../stix_shifter_modules/carbonblack/carbonblack_supported_stix.md)
- [Carbon Black Cloud](../stix_shifter_modules/cbcloud/cbcloud_supported_stix.md)
- [Cisco Secure Email](../stix_shifter_modules/cisco_secure_email/cisco_secure_email_supported_stix.md)
- [CrowdStrike Falcon](../stix_shifter_modules/crowdstrike/crowdstrike_supported_stix.md)
- [CrowdStrike Falcon Alerts API](../stix_shifter_modules/crowdstrike_alerts/crowdstrike_alerts_supported_stix.md)
- [Cybereason](../stix_shifter_modules/cybereason/cybereason_supported_stix.md)
- [Darktrace](../stix_shifter_modules/darktrace/darktrace_supported_stix.md)
- [Datadog](../stix_shifter_modules/datadog/datadog_supported_stix.md)
- [Elasticsearch ECS](../stix_shifter_modules/elastic_ecs/elastic_ecs_supported_stix.md)
- [GCP Chronicle](../stix_shifter_modules/gcp_chronicle/gcp_chronicle_supported_stix.md)
- [IBM Guardium Data Protection](../stix_shifter_modules/guardium/guardium_supported_stix.md)
- [IBM Security Verify](../stix_shifter_modules/ibm_security_verify/ibm_security_verify_supported_stix.md)
- [Microsoft Defender for Endpoint](../stix_shifter_modules/msatp/msatp_supported_stix.md)
- [Okta](../stix_shifter_modules/okta/okta_supported_stix.md)
- [OneLogin](../stix_shifter_modules/onelogin/onelogin_supported_stix.md)
- [PaloAlto Cortex XDR](../stix_shifter_modules/paloalto/paloalto_supported_stix.md)
- [Proofpoint (SIEM API)](../stix_shifter_modules/proofpoint/proofpoint_supported_stix.md)
- [IBM Security QRadar SIEM](../stix_shifter_modules/qradar/qradar_supported_stix.md)
- [IBM Security QRadar EDR](../stix_shifter_modules/reaqta/reaqta_supported_stix.md)
- [Red Hat Advanced Cluster Security for Kubernetes](../stix_shifter_modules/rhacs/rhacs_supported_stix.md)
- [IBM Security Verify Privilege Vault](../stix_shifter_modules/secretserver/secretserver_supported_stix.md)
- [SentinelOne](../stix_shifter_modules/sentinelone/sentinelone_supported_stix.md)
- [Splunk Enterprise Security](../stix_shifter_modules/splunk/splunk_supported_stix.md)
- [Sumo Logic](../stix_shifter_modules/sumologic/sumologic_supported_stix.md)
- [Trend Micro Vision One](../stix_shifter_modules/trendmicro_vision_one/trendmicro_vision_one_supported_stix.md)
- [Vectra NDR](../stix_shifter_modules/vectra/vectra_supported_stix.md)
- [Sysdig](../stix_shifter_modules/sysdig/sysdig_supported_stix.md)
