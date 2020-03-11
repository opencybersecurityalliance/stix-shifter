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

- [QRadar](connectors/qradar_supported_stix.md)
- [Splunk Enterprise Security](connectors/splunk_supported_stix.md)
- [BigFix](connectors/bigfix_supported_stix.md)
- [Carbon Black CB Response](connectors/carbonblack_supported_stix.md)
- [Elasticsearch ECS](connectors/elastic_ecs_supported_stix.md)
- [Microsoft Defender Advanced Threat Protection](connectors/msatp_supported_stix.md)
- [IBM Cloud Security Advisor](connectors/security_advisor_supported_stix.md)
- [IBM Security Guardium](connectors/guardium_supported_stix.md)
- [Amazon CloudWatch Logs](connectors/aws_cloud_watch_logs_supported_stix.md)
- [Microsoft Azure Sentinel](connectors/azure_sentinel_supported_stix.md)
