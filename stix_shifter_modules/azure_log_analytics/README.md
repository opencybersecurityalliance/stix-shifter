# Azure Log Analytics

## Supported STIX Mappings

See the [table of mappings](azure_log_analytics_supported_stix.md) for the STIX objects and operators supported by this connector.

## Data Source 
Microsoft Azure Log Analytics is a tool to run queries on data collected by different Azure services. A Log Analytics workspace needs to be created to collect logs from Azure services. The connector can run Kusto Query Language (KQL) queries to search logs in the workspace.

## API and Logs

Currently, [Log Analytics REST API](https://learn.microsoft.com/en-us/rest/api/loganalytics/) has been used to search three types of Azure Sentinel logs:

1. Security Alert
2. Security Events 
3. Security Incidents

Therefore, three dialects has been set in the from_stix mapping file. More data tables will be supported in future.

Azure SDK for Python is used in order to make API calls to Log Analytics API. Mainly two libraries are used:

1. [Azure Identity library](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python)
    - It mainly enables the Azure SDK clients to authenticate with AAD
2. [Azure Monitor Query client library](https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python)
    - It provides functions to run quries on the logs availabe in Azure Sentinel
    - [Kusto Query Language (KQL)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/) has been used as a query language to run search using this client.

### Format for calling stix-shifter from the command line

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Example I - Converting from STIX patterns to KQL (STIX attributes)
STIX to KQL field mapping is defined in `<dialects>_from_stix_map.json` <br/>

This example input pattern:

`translate azure_log_analytics query ‘{}’ "[process:name = 'svchost.exe'] START t'2019-01-01T08:43:10Z' STOP t'2019-12-31T08:43:10Z'"`

Returns the following translated query:

```
{
    "queries": [
        "SecurityEvent | where (IpAddress == '1.1.1.1') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))"
    ]
}
```

### Example II - Converting from STIX patterns to KQL Custom STIX attributes)

This example input pattern:

`translate azure_log_analytics query ‘{}’ "[x-ibm-finding:name = 'Microsoft-Windows-Security-Auditing'] START t'2019-01-01T08:43:10Z' STOP t'2019-12-31T08:43:10Z'"`

Returns the following translated queries:
```
{
    "queries": [
        "SecurityEvent | where (EventSourceName == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))",
        "SecurityIncident | where (IncidentName == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))",
        "SecurityAlert | where (AlertName == 'Microsoft-Windows-Security-Auditing') and (TimeGenerated between (datetime(2019-01-01T08:43:10Z) .. datetime(2019-12-31T08:43:10Z)))"
    ]
}```