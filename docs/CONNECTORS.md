[qradar]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/qradar
[qradar_on_cloud]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/qradar
[bigfix]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/bigfix
[carbonblack]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/carbonblack
[cbcloud]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/cbcloud
[elastic_ecs]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/elastic_ecs
[security_advisor]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/security_advisor
[splunk]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/splunk
[msatp]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/msatp
[azure_sentinel]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/azure_sentinel
[guardium]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/guardium
[aws_cloud_watch_logs]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/aws_cloud_watch_logs
[aws_athena]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/aws_athena
[alertflex]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/alertflex
[arcsight]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/arcsight
[crowdstrike]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/crowdstrike
[trendmicro_vision_one]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/trendmicro_vision_one
[secretserver]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/secretserver
[onelogin]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/onelogin
[mysql]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/mysql
[sumologic]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/sumologic
[datadog]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/datadog
[infoblox]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/infoblox
[proofpoint]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/proofpoint
[cybereason]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/cybereason
[paloalto]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/paloalto
[sentinelone]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/sentinelone
[darktrace]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/darktrace
[reaqta]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/reaqta
[ibm_security_verify]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/ibm_security_verify
[rhacs]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/rhacs
[gcp_chronicle]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/gcp_chronicle
[azure_log_analytics]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/azure_log_analytics
[okta]: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/okta


# Available Connectors

STIX-shifter currently offers connector support for the following cybersecurity products.

List updated: April 18, 2023

|       |         Connector          |      Module Name     | Data Model |  Developer   | Translation | Transmission | Availability |
| :---: | :------------------------: | :------------------: | :--------: | :----------: | :---------: | :----------: | :----------: |
|   01  |         [IBM QRadar][qradar]         |        qradar        |  QRadar AQL   | IBM Security |     Yes     |     Yes      |   Released    |
|   02  |    [IBM QRadar on Cloud][qradar_on_cloud]    |        qradar        | QRadar AQL | IBM Security |     Yes     |     Yes      |   Released    |
|   03  |         [HCL BigFix][bigfix]        |        bigfix        |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   04  |  [Carbon Black CB Response][carbonblack]  |      carbonblack     |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   05  |  [Carbon Black Cloud][cbcloud]  |      cbcloud     |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   06  |       Elasticsearch       |       elastic        | MITRE CAR  |    MITRE     |     Yes     |      No      |   Released    |
|   07  |       [Elasticsearch (ECS)][elastic_ecs]       |     elastic_ecs      |    ECS     | IBM Security |     Yes     |     Yes      |   Released    |
|   08  | [IBM Cloud Security Advisor][security_advisor] |   security_advisor   |  Default   |  IBM Cloud   |     Yes     |     Yes      |   Released    |
|   09  |           [Splunk Enterprise Security][splunk]           |        splunk        | Splunk CIM | IBM Security |     Yes     |     Yes      |   Released    |
|   10  |       [Microsoft Defender for Endpoint][msatp]        |        msatp         |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   11  |       [Microsoft Graph Security][azure_sentinel]     |    azure_sentinel    |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   12  |        [IBM Guardium Data Protection][guardium]     |       guardium       |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   13  |    [AWS CloudWatch Logs][aws_cloud_watch_logs]     | aws_cloud_watch_logs |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   14  |       [Amazon Athena][aws_athena]       |   aws_athena   |  SQL   | IBM Security |     Yes     |     Yes      |   Released    |
|   15  |       [Alertflex][alertflex]       |    alertflex    |  Default   | Alertflex |     Yes     |     Yes      |   Released    |
|   16  |       [Micro Focus ArcSight][arcsight]       |    arcsight    |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   17  |       [CrowdStrike Falcon][crowdstrike]       |    crowdstrike    |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   18  |       [Trend Micro Vision One][trendmicro_vision_one]       |    trendmicro_vision_one    |  Default   | Trend Micro |     Yes     |     Yes      |   Released    |
|   19  |       [IBM Security Verify Privilege Vault][secretserver]       |    secretserver    |  Default   | IBM |     Yes     |     Yes      |   Released    |
|   20  |       [One Login][onelogin]       |    onelogin    |  Default   | GS Lab |     Yes     |     Yes      |   Released    |
|   21  |       [MySQL][mysql]                                                                  |    mysql    |  Default   | IBM |     Yes     |     Yes      |   Released    |
|   22  |       [Sumo Logic][sumologic]       |    sumologic    |  Default   | GS Lab |     Yes     |     Yes      |   Released    |
|   23  |       [Datadog][datadog]       |    datadog    |  Default   | GS Lab |     Yes     |     Yes      |   Released    |
|   24  |       [Infoblox BloxOne Threat Defense][infoblox]       |    infoblox    |  Default   | Infoblox |     Yes     |     Yes      |   Released    |
|   25  |       [Proofpoint (SIEM API)][proofpoint]       |    proofpoint    |  Default   | IBM Security |     Yes     |     Yes      |   Released    |
|   26  |       [Cybereason][cybereason]                        | cybereason              | Default    | IBM Security | Yes         | Yes          | Released     |
|   27  |       [Palo Alto Cortex XDR][paloalto]                        | paloalto              | Default    | IBM Security | Yes         | Yes          | Released     |
|   28  |       [SentinelOne][sentinelone]                        | sentinelone              | Default    | IBM Security | Yes         | Yes          | Released     |
|   29  |       [Darktrace][darktrace]                           | darktrace              | Default    | IBM Security | Yes         | Yes          | Released     |
|   30  |       [IBM Security QRadar EDR][reaqta]                           | reaqta             | Default    | IBM Security | Yes         | Yes          | Released     |
|   31  |       [IBM Security Verify][ibm_security_verify]                           | ibm_security_verify             | Default    | IBM Security | Yes         | Yes          | Released     |
|   32  |       [Red Hat Advanced Cluster Security for Kubernetes (StackRox)][rhacs]                           | rhacs             | Default    | IBM Security | Yes         | Yes          | Released     |
|   33  |      [GCP Chronicle][gcp_chronicle]                   | gcp_chronicle              | Default    | IBM Security | Yes         | Yes          | Released     |
|   34  |      [Azure Log Analytics][azure_log_analytics]                   | azure_log_analytics              | Default    | IBM Security | Yes         | Yes          | Released     |
|   35  |      [Okta][okta]                   | okta              | Default    | IBM Security | Yes         | Yes          | Released     |

